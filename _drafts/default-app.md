
cytrinox@pollux ~ $ vim .local/share/applications/mimeapps.list 
cytrinox@pollux ~ $ xdg-mime query default application/pdf
libreoffice-draw.desktop
cytrinox@pollux ~ $ xdg-mime default 
xdg-mime: application argument missing
Try 'xdg-mime --help' for more information.
cytrinox@pollux ~ $ xdg-mime default evince.desktop application/pdf
cytrinox@pollux ~ $ xdg-mime query default application/pdf

