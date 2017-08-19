import vk_api
import acc
import os
import datetime
import urllib.request

def date(date_):
    return datetime.datetime.fromtimestamp(int(date_)).strftime('%d-%m-%Y %H:%M:%S')

def main():
    login = acc.login
    password = acc.password
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    
    vk = vk_session.get_api()
    gList = vk.groups.get()
    g_id = int(input('Enter the group number in your group list:')) - 1
    group = gList['items'][g_id]
    count_ = vk.wall.get(owner_id = -group)['count']
    k = 0
    pcount_ = 0
    print('predprocessing...\n')
    while k < count_:
        print(str(k) + '/' + str(count_))
        gwall = vk.wall.get(owner_id = -group, count = 100, offset = k)
        for post_ in gwall['items']:
            if post_.get('attachments') == None:
                continue
            for file_ in post_['attachments']:
                if file_['type'] == 'photo':
                    pcount_ += 1
        k += 100
    print('Beginning downloading:\n')
    k = 0
    cur = 0
    ptypes = ['photo_2560', 'photo_1280', 'photo_807', 'photo_604', 'photo_130', 'photo_75']
    if not os.path.exists('photos'):
        os.makedirs('photos')
    while k < count_:
        gwall = vk.wall.get(owner_id = -group, count = 100, offset = k)
        for post_ in gwall['items']:
            if post_.get('attachments') == None:
                continue
            pcnt = 0
            for file_ in post_['attachments']:
                if file_['type'] == 'photo':
                    pcnt += 1
                    cur += 1
                    for sz in ptypes:
                        if file_['photo'].get(sz):
                            name_ = date(post_['date']) + '_' + str(pcnt) + '.jpg'
                            url_ = file_['photo'][sz]
                            urllib.request.urlretrieve(url_, 'photos/' + name_)
                            print(url_ + ' saved as ' + name_)
                            break
            print('-->' + str(cur / pcount_ * 100) + '% Done')
        k += 100

if __name__ == '__main__':
    main()

