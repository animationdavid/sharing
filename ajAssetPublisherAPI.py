import os

C_ANCHOR_PATH = None
C_ASSETS_FOLDER_NAME = "assets"
C_GEO_FORMAT_SUPPORTED = ["abc", "usd"]
C_ASSETS_DATA = None

def getAnchorPath(node):
    '''
    Return the prefix path for the project, by default: $HIP
    '''
    if C_ANCHOR_PATH != None:
        return C_ANCHOR_PATH
    else:
        return node.parm("anchor_path").evalAsString()

def getAssets(node):
    '''
    Return a dict with all the asset information based on the project structure folder.
    '''
    import glob
    
    anchor_path = getAnchorPath(node)
    asset_type = getSelectedAssetType(node)

    assets = {}
    
    assets_folder = os.path.join(anchor_path, C_ASSETS_FOLDER_NAME, asset_type)
    
    for name in os.listdir(assets_folder):
        
        asset_path = os.path.join(assets_folder, name)
        
        if not os.path.isdir(asset_path):
            continue

        for root, dirs, files in os.walk(asset_path):
            files = [f for f in files if f.split(".")[1] in C_GEO_FORMAT_SUPPORTED]
            assets[name] = {"root":root,"files":files}
    
    return assets

def getSelectedAssetData(asset_name):

    return C_ASSETS_DATA.get(asset_name)

def getAssetGeos(asset_name):

    asset = getSelectedAssetData(asset_name)

    root_path = asset.get("root")
    cache_files = asset.get("files")

    if not cache_files:
        return []

    return [os.path.normpath(os.path.join(root_path, f)) for f in cache_files]

def getAssetTypes(node):
    '''
    Return a list names of asset types based on the project structure folder
    '''
    anchor_path = getAnchorPath(node)
    
    path = os.path.join(anchor_path, C_ASSETS_FOLDER_NAME)
    
    return [dir for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))]

def getSelectedAssetType(node):
    '''
    Return the current asset type selected
    '''

    return node.parm("asset_type").evalAsString()

def getSelectedAsset(node):
    '''
    Return the current asset selection
    '''
    
    return node.parm("asset_name").evalAsString()

def setAssetsMenu(node):
    '''
    Fills assets menu with a list of strings
    '''
    return_list = []
    
    assets = C_ASSETS_DATA.keys()
        
    if not assets:
        return return_list
    
    for asset_name in assets:
        return_list.append(asset_name)
        return_list.append(asset_name)
    
    return return_list

def setAssetTypeMenu(node):
    '''
    Fills asset type menu with a list of strings
    '''
    return_list = []
   
    asset_types = getAssetTypes(node)

    if asset_types:
        for s in asset_types:
            return_list.append(s)
            return_list.append(s)
    

    return return_list
    
def setCachesMenu(node):
    '''
    Fills assets menu with a list of strings
    '''    
    return_list = []
    
    current_asset = getSelectedAsset(node)
    cache_paths = getAssetGeos(current_asset)
        
    for path in cache_paths:
        return_list.append(path)
        return_list.append(path)


    return return_list

def resetAssetParameters(node):
    '''
    Function to reset asset parameters
    '''
    node.parm("asset_name").set("")
    node.parm("cache_file").set("")

def setCacheFileParm(node):
    '''
    '''
    current_asset = getSelectedAsset(node)
    cache_path = getAssetGeos(current_asset)[0]

    node.parm("cache_file").set(cache_path)

    return True

def fillData(node):
    '''
    Main function to gather all the assets data, this function is executed once we have selecected an asset in the UI 
    and fills a global variable with a dictionary.
    '''
    global C_ASSETS_DATA
    resetAssetParameters(node)
    C_ASSETS_DATA = getAssets(node)

    return True


#### TESTING FUNCTIONS ####

def testGetAssets():
    print(C_ASSETS_DATA)
