# Extract Broadlink IR/RF codes from iOS App
- 博联RM Pro+智能遥控，学习到的红外/射频码的，最简单获取方式。
- I want fxxk Broadlink first, for waste me so many time in learning RF code.
- And I accidentally found a very convenient method to get these codes.
- It works for me, and hope it helps you.

# 1. Create scene contains all commands
- Create a scene in `BroadLink App` ([this one](https://apps.apple.com/us/app/broadlink/id1450257910)), my version is 1.2.3 from appstore Japan.
- Created `ALL RF Devices', and please add all the commands you need.  
    ![scene](readme_img/scene.png)

# 2. Get database with iTunes 
- Open your iTunes, and connect your phone.
- In file sharing, find `BroadLink` App, and save `BLDataManager.sqlite` to your disk.  
    ![](readme_img/itunes.png)

# 3. Read database and find YOUR codes
- Yes, the codes should belong to you, not BroadLink only. (I am really mad about it.)
- Fine, you can open it with some sqlite GUI, I used [DB Browser for SQLite](https://sqlitebrowser.org/).
- In `BL_SceneDevInfo_List`, the `content` column contains all the codes we need.
- But just the commands what added to `Scene` (in step 1) contains. (Here contains all the scenes, but maybe some command not belong to any scene, so I add them in step 1.)  
    ![](readme_img/sqlite.png)
- If you only need a few pieces of code, you can copy and convert it to base64.

# 4. Extract all codes by python
- Export the `BL_SceneDevInfo_List` to a json file, I've shared mine as a sample.
- And run the python file `extract_codes.py`, make sure this two files are in same folder. And it's python3.
- Then it will auto save a `codes.txt` in save folder, contains all the codes, converted into base64. You can directly test it in hass service.

# It's not perfect
- I don't want share all my database, so we operate a exported json file. (Hope there is nothing sensitive in it.)
- And in the `codes.txt`, you can identify commands by `name` & `func`, because I can not translate `device id` to `device name`, it need whole database or export more json, forget it please.
- In sample files, many name display in Chinese, but that should not cause trouble, right?
- Hope this helps, and good luck!
