import os

class Tree:
    def __init__(self):
        pass

    def listFiles(startpath,groupName):
        treeList = [] # [0]:Name [1]:Id [2]:Parent [3]:Path [4]:Type (file / folder)
        treeLevelsList = []
        line = []
        index = 0
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 1 * (level)
            folderName = os.path.basename(root)

            levelList = [groupName+":"+str(index)+":"+folderName]

            if len(treeLevelsList) < level+1:
                treeLevelsList.append(levelList)
            else:
                treeLevelsList[level] = levelList

            if (level == 0):
                # line = [folderName,groupName+":"+str(index)+":"+folderName,groupName,""]
                line = [folderName,groupName+":"+str(index)+":"+folderName,groupName,os.path.abspath(root).replace("\\","/"),"folder"]
            else:
                # line = [folderName,groupName+":"+str(index)+":"+folderName,treeLevelsList[level-1][0],""]
                line = [folderName,groupName+":"+str(index)+":"+folderName,treeLevelsList[level-1][0],os.path.abspath(root).replace("\\","/"),"folder"]
            treeList.append(line)

            subindent = ' ' * 1 * (level + 1)
            for f in files:
                index += 1
                line = [f,groupName+":"+str(index)+":"+f,treeLevelsList[level][0],os.path.join(os.path.abspath(root),f).replace("\\","/"),"file"]
                treeList.append(line)
            index += 1
        return treeList



if __name__ == "__main__":
    t = Tree.listFiles("./root","TTR")
    for x in t:
        print(x)
    pass