#!/bin/bash
# Fix git remotes — GitHub SSH is primary, GitLab is for backup only
cd /home/mingo/echo-v1-brain
git remote set-url origin git@github.com:Liberty-Emporium/echo-v1.git
git remote remove gitlab 2>/dev/null
echo "Remotes updated. Origin (GitHub SSH) is primary."
git remote -v
