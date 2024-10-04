from maya import cmds


def locator_from_ctrl_and_bake(root_name, ctr_name):
    # clear all selection
    cmds.select([])
    
    # find the controler
    result = None
    for obj in cmds.ls(l=True, dag=True):
        if root_name in obj and ctr_name in obj:
            result = obj
            break
    if not result:
        print("Cannot find the object in filtered scope")
        return
    
    # get start and end frames of playbar
    start_frame = cmds.playbackOptions(q=True, min=True)
    end_frame = cmds.playbackOptions(q=True, max=True)
    
    # set current time to the first frame
    cmds.currentTime(start_frame, e=True)
    
    # create a locator and constraint to target
    locator = cmds.spaceLocator()
    pc = cmds.parentConstraint(result, locator)
    
    # select the new locator
    cmds.select(locator)
    
    # bake controller and remove constraint
    cmds.bakeResults(sm=True, sr=True, t=(start_frame, end_frame))
    cmds.delete(cn=True)
    
    # rename the locator
    locator = cmds.rename(locator, "LCT_{pref}_{suf}".format(pref=root_name, suf=ctr_name))
    
    return locator

            
            
# specify filter names:
new_locator = locator_from_ctrl_and_bake(root_name="bob", ctr_name="SomeHip_CTR")

# TODO: write the export
        