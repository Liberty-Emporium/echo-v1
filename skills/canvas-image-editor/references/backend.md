# Canvas Image Editor — Flask Backend Reference

## File Paths Setup (Railway-safe)
```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_vol     = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', '')
DATA_DIR = os.environ.get('DATA_DIR', _vol if _vol else BASE_DIR)
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
```

## Serve Uploads (404-safe)
```python
@app.route('/uploads/<filename>')
def serve_upload(filename):
    fp = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(fp):
        import base64 as _b64
        from flask import Response
        px = _b64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=')
        return Response(px, status=404, mimetype='image/png', headers={'X-Upload-Missing': filename})
    return send_from_directory(UPLOAD_FOLDER, filename)
```

## Save Edited Image
```python
@app.route('/save-image/<sku>', methods=['POST'])
@login_required
def save_image(sku):
    data = request.get_json(force=True)
    image_data = data.get('image_data', '')
    filename   = data.get('filename', '')
    if image_data and filename:
        header, encoded = image_data.split(',', 1)
        img_bytes = base64.b64decode(encoded)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, 'wb') as f: f.write(img_bytes)
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Missing image_data or filename'})
```

## Upload New Photo
```python
@app.route('/upload-photo/<sku>', methods=['POST'])
@login_required
def upload_photo(sku):
    products = load_inventory()
    product  = next((p for p in products if p['SKU'] == sku), None)
    if not product: return jsonify({'error': 'Product not found'})
    results = []
    for file in request.files.getlist('photos'):
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            fname = f"{sku}_{uuid.uuid4().hex[:8]}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, fname))
            existing = [i.strip() for i in (product.get('Images') or '').split(',') if i.strip()]
            existing.append(fname)
            product['Images'] = ','.join(existing)
            results.append({'filename': fname, 'url': url_for('serve_upload', filename=fname)})
    save_inventory(products)
    return jsonify({'success': True, 'uploaded': results})
```

## Delete Image
```python
@app.route('/delete-image/<sku>', methods=['POST'])
@login_required
def delete_image(sku):
    data = request.get_json(force=True) or {}
    filename = data.get('filename') or request.form.get('filename')
    products = load_inventory()
    idx = next((i for i, p in enumerate(products) if p['SKU'] == sku), None)
    if idx is not None and filename:
        imgs = [i.strip() for i in products[idx].get('Images','').split(',') if i.strip()]
        if filename in imgs:
            imgs.remove(filename)
            products[idx]['Images'] = ','.join(imgs)
            save_inventory(products)
        fp = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(fp): os.remove(fp)
    return jsonify({'success': True})
```

## Reorder Images
```python
@app.route('/reorder-images/<sku>', methods=['POST'])
@login_required
def reorder_images(sku):
    data  = request.get_json(force=True)
    order = data.get('order', [])   # list of filenames in new order
    products = load_inventory()
    idx = next((i for i, p in enumerate(products) if p['SKU'] == sku), None)
    if idx is not None:
        products[idx]['Images'] = ','.join(order)
        save_inventory(products)
    return jsonify({'success': True})
```

## Standard Background Removal (rembg, whole image)
```python
@app.route('/enhance-image/<sku>', methods=['POST'])
@login_required
def enhance_image(sku):
    import io as _io
    from PIL import Image as _Img
    from rembg import remove as rembg_remove
    products = load_inventory()
    product  = next((p for p in products if p['SKU'] == sku), None)
    if not product: return jsonify({'error': 'Product not found'})
    filename = (request.get_json(force=True) or {}).get('filename', '')
    if not filename:
        imgs = [i.strip() for i in (product.get('Images') or '').split(',') if i.strip()]
        filename = imgs[0] if imgs else ''
    if not filename: return jsonify({'error': 'No image found'})
    fp = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(fp): return jsonify({'error': 'File not found'})
    img_bytes    = open(fp, 'rb').read()
    result_bytes = rembg_remove(img_bytes, alpha_matting=True,
                                alpha_matting_foreground_threshold=240,
                                alpha_matting_background_threshold=10,
                                alpha_matting_erode_size=10)
    result = _Img.open(_io.BytesIO(result_bytes)).convert('RGBA')
    white  = _Img.new('RGBA', result.size, (255,255,255,255))
    white.paste(result, mask=result.split()[3])
    final  = white.convert('RGB')
    pad    = int(max(final.size) * 0.05)
    padded = _Img.new('RGB', (final.width+pad*2, final.height+pad*2), (255,255,255))
    padded.paste(final, (pad, pad))
    base = os.path.splitext(filename)[0]
    new_fn = f"{base}_white_bg.jpg"
    padded.save(os.path.join(UPLOAD_FOLDER, new_fn), format='JPEG', quality=92)
    existing = [i.strip() for i in (product.get('Images') or '').split(',') if i.strip()]
    if new_fn in existing: existing.remove(new_fn)
    existing.insert(0, new_fn)
    product['Images'] = ','.join(existing)
    save_inventory(products)
    return jsonify({'success': True, 'filename': new_fn, 'url': url_for('serve_upload', filename=new_fn)})
```

## Guided Background Removal (user bbox → protect product pixels)
```python
@app.route('/guided-remove-bg/<sku>', methods=['POST'])
@login_required
def guided_remove_bg(sku):
    """
    POST JSON: {"filename": "foo.jpg", "box": {"x": 0.1, "y": 0.05, "w": 0.8, "h": 0.9}}
    box values are 0-1 fractions of image dimensions.
    Strategy: run rembg on full image with alpha matting, then force alpha=255 inside
    user's box so product pixels are never accidentally erased.
    """
    import io as _io
    import PIL.ImageDraw as _IDraw, PIL.ImageChops as _IChops
    from PIL import Image as _Img
    from rembg import remove as rembg_remove
    products = load_inventory()
    product  = next((p for p in products if p['SKU'] == sku), None)
    if not product: return jsonify({'error': 'Product not found'})
    data     = request.get_json(force=True)
    filename = (data or {}).get('filename', '')
    box      = (data or {}).get('box', {})
    fp = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(fp): return jsonify({'error': 'File not found'})
    orig = _Img.open(fp).convert('RGB')
    W, H = orig.size
    x1 = max(0, int(float(box.get('x',0.05)) * W))
    y1 = max(0, int(float(box.get('y',0.05)) * H))
    x2 = min(W, int((float(box.get('x',0.05)) + float(box.get('w',0.9))) * W))
    y2 = min(H, int((float(box.get('y',0.05)) + float(box.get('h',0.9))) * H))
    img_bytes    = open(fp, 'rb').read()
    result_bytes = rembg_remove(img_bytes, alpha_matting=True,
                                alpha_matting_foreground_threshold=250,
                                alpha_matting_background_threshold=5,
                                alpha_matting_erode_size=8)
    result_rgba = _Img.open(_io.BytesIO(result_bytes)).convert('RGBA')
    r, g, b, a  = result_rgba.split()
    protect     = _Img.new('L', (W, H), 0)
    _IDraw.Draw(protect).rectangle([x1, y1, x2, y2], fill=255)
    merged_a    = _IChops.lighter(a, protect)   # max(rembg_alpha, box_alpha)
    result_rgba = _Img.merge('RGBA', (r, g, b, merged_a))
    white = _Img.new('RGBA', result_rgba.size, (255,255,255,255))
    white.paste(result_rgba, mask=result_rgba.split()[3])
    final  = white.convert('RGB').crop((max(0,x1-20), max(0,y1-20), min(W,x2+20), min(H,y2+20)))
    base   = os.path.splitext(filename)[0]
    new_fn = f"{base}_guided_bg.jpg"
    final.save(os.path.join(UPLOAD_FOLDER, new_fn), format='JPEG', quality=92)
    existing = [i.strip() for i in (product.get('Images') or '').split(',') if i.strip()]
    if new_fn in existing: existing.remove(new_fn)
    existing.insert(0, new_fn)
    product['Images'] = ','.join(existing)
    save_inventory(products)
    return jsonify({'success': True, 'filename': new_fn, 'url': url_for('serve_upload', filename=new_fn)})
```
