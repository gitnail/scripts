import vk_api
import acc
import datetime

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
    group = gList['items'][0]
    count_ = vk.wall.get(owner_id = -group)['count']
    k = 0
    cur = 0
    f = open('allposts.txt', 'w')
    f.write('Количество постов = ' + str(count_) + '\n\n')
    fnames = {}
    lnames = {}
    while k < count_:
        gwall = vk.wall.get(owner_id = -group, count = 100, offset = k)
        for post_ in gwall['items']:
            autorId = post_['from_id']
            if autorId < 0:
                name = 'Группа:'
            else:
                if fnames.get(autorId) == None:
                    fnames[autorId] = vk.users.get(user_ids = autorId)[0]['first_name']
                    lnames[autorId] = vk.users.get(user_ids = autorId)[0]['last_name']
                name = fnames[autorId]
                name += ' ' + lnames[autorId] + ':'
            date_ = post_['date']
            f.write(name + '\n')
            f.write(date(date_) + '\n')
            f.write(post_['text'] + '\n' + '\n')
            cur += 1
            print(str(cur / count_ * 100) + '%' + ' done')
        k += 100
    print(cur)
    f.close()
if __name__ == '__main__':
    main()
