import win32com.client
SILENT_CLOSE = 2
# This actually fires up Photoshop if not already running.
psApp = win32com.client.Dispatch("Photoshop.Application")
psApp.DisplayDialogs = 3            # psDisplayNoDialogs
psApp.Preferences.RulerUnits = 1    # psPixels

smartObjects = []
# Open an image file (PSD in our case)
image_t_shirt=r"C:\Users\Lam\Pictures\BlueStacks\447857-PF1FKN-86-02.png"
target = psApp.Open(image_t_shirt)
star = target.Duplicate()
star_layer = star.ArtLayers.Item(1)
star_layer.Copy()
psApp.Open(r"C:\Users\Lam\Pictures\BlueStacks\t-shirt-mock-up-design\OJYV111.psd")
psDoc=psApp.Application.ActiveDocument

layer=psDoc.ArtLayers.Item(1)
psDoc.activeLayer = psDoc.ArtLayers.Item(1)
# psApp.executeAction(psApp.stringIDToTypeID("placedLayerEditContents"))
smartDoc = psApp.activeDocument
psApp.ActiveDocument =layer
layer.Paste()
layer.Save()


for layerGrp in psDoc.layerSets:
    for layer in layerGrp.artLayers:
        if layer.kind == 17:  # 17 means it's a smart object
            smartObjects.append(layer)
for layer in smartObjects:
        try:
            psDoc.activeLayer = layer
            psApp.executeAction(psApp.stringIDToTypeID("placedLayerEditContents"))
            smartDoc = psApp.activeDocument
            smartDoc.Paste()
            print('Run some function here on the smart object')
            smartDoc.save()
            smartDoc.close()
            # after closing the smartDoc the main psd will now be the active document

        except:
            print( 'passed on something here.')
            pass
# background = doc.Duplicate()
# mockup_layer=background.ArtLayers
# ps.Open(mockup_layer)
# image_t_shirt=r"C:\Users\Lam\Pictures\BlueStacks\447857-PF1FKN-86-02.png"
#
# target = ps.Open(image_t_shirt)
# star = target.Duplicate()
# target.Close(SILENT_CLOSE)


# for layer in doc:
#
#     if layer.kind == "smartobject":
#         print("SFDSDFD")
# ... do something ...
# doc.Close()

# ps.Quit() # Stops the Photoshop application