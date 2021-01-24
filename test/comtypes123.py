import comtypes.client as ct
psApp = ct.CreateObject('Photoshop.Application', dynamic=True)
psApp.Visible = True
image_t_shirt=r"C:\Users\Lam\Pictures\BlueStacks\447857-PF1FKN-86-02.png"
target = psApp.Open(image_t_shirt)

target_layer = target.ArtLayers.Item(1)
target_layer.Copy()



psApp.Open(r"C:\Users\Lam\Pictures\BlueStacks\t-shirt-mock-up-design\OJYV111.psd")
psDoc=psApp.Application.ActiveDocument
layer=psDoc.ArtLayers.Item(1)
psDoc.activeLayer = psDoc.ArtLayers.Item(1)
psApp.executeAction(psApp.stringIDToTypeID("placedLayerEditContents"))
# psApp.executeAction(psApp.stringIDToTypeID("placedLayerEditContents"))
smartDoc = psApp.activeDocument

smartDoc.Paste()
# creates com object for tga save operation
tga_save_options = ct.CreateObject(
    'Photoshop.PngSaveOptions', dynamic=True)
# tga_save_options.Format = 13  # PNG
# tga_save_options.PNG8 = False

# If designated to include alpha, set parameters to do so




gen_path = r"dataset\finalx.png"
psApp.activeDocument.SaveAs(gen_path, tga_save_options, True)
psApp.activeDocument.save()
psApp.activeDocument.close()