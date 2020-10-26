from linebot import LineBotApi
import json
# step0 創建line_bot_api
line_bot_api = LineBotApi("m56TRmt+7nk5XEjKuSQnf2wv4WatylCZY5PQxo3eG5dOGGuxFHGGrLGPFagNdVOLrD4qh++Pft+Ks8q9qZcGhzKhH/9QasYV/arh2XO+wxF9jG1Bp8qOvUxC8hP+1fN0mGEM/A+Sh2CD6FgY1sRkGAdB04t89/1O/w1cDnyilFU=")


rich_menu_string ="""{
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": true,
  "name": "圖文選單 1",
  "chatBarText": "查看更多資訊",
  "areas": [
    {
      "bounds": {
        "x": 8,
        "y": 0,
        "width": 825,
        "height": 698
      },
      "action": {
        "type": "message",
        "text": "其他功能"
      }
    },
    {
      "bounds": {
        "x": 850,
        "y": 8,
        "width": 807,
        "height": 682
      },
      "action": {
        "type": "message",
        "text": "該看哪一科"
      }
    },
    {
      "bounds": {
        "x": 1691,
        "y": 8,
        "width": 799,
        "height": 673
      },
      "action": {
        "type": "uri",
        "uri": "https://example.com/"
      }
    },
    {
      "bounds": {
        "x": 0,
        "y": 702,
        "width": 833,
        "height": 686
      },
      "action": {
        "type": "uri",
        "uri": "https://example.com/"
      }
    },
    {
      "bounds": {
        "x": 850,
        "y": 715,
        "width": 807,
        "height": 681
      },
      "action": {
        "type": "uri",
        "uri": "https://example.com/"
      }
    },
    {
      "bounds": {
        "x": 1691,
        "y": 707,
        "width": 799,
        "height": 698
      },
      "action": {
        "type": "uri",
        "uri": "tel://034257387"
      }
    }
  ]
}"""
# drap the pic into the folder


# step1 用json, 製作圖文選單
# 執行一次就可
rich_menu_json = json.loads(rich_menu_string)
from linebot.models.rich_menu import RichMenu
rich_menu_id = line_bot_api.create_rich_menu(
    rich_menu=RichMenu.new_from_json_dict(rich_menu_json)
)
print("rich_menu_id")
print(rich_menu_id)


# step2 上傳圖片至選單
#  讀取圖片
# 執行一次即可
rich_menu_file = open("rich_menu.jpg", 'rb')

# 上傳給line
# set_rich_menu_image('圖文選單id', 'image/jpeg', 圖片)
# 執行一次即可
line_bot_api.set_rich_menu_image("richmenu-8b955072ab003e314754f16ebb41ab51", "image/jpeg", rich_menu_file)


# step 3 將選單對用戶作綁定df
import json
json_object_strings = open("./users.txt", "r")
json_array = []
user_id_array = []
for json_object_string in json_object_strings:
    json_object = json.loads(json_object_string)
    json_array.append(json_object)

for user_record in json_array:
    user_id_array.append(user_record.get("user_id"))
line_bot_api.link_rich_menu_to_user(user_id_array, 'richmenu-8b955072ab003e314754f16ebb41ab51')

# step 4 解除綁定
# line_bot_api.unlink_rich_menu_from_users(user_ids=user_id_array)

# step 5 檢視所有圖文選單
demo = line_bot_api.get_rich_menu_list()
for i in demo:
    print(i)