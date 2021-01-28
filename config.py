
var client_id = "a4a8320b97e84b88bc8f4585251085ce"
var user_id = '1221063701'
var client_secret = '57f7dc998a714c61b8391858bdc5cc7c'
var playlist_id = '0fCFwL8LJE99raQb1g2YvF?si=LRMrE3NVQxqq8CZ2Nlb6QQ'
var redirect_uri='https://www.facebook.com/groups/1223037501082162'

token = util.prompt_for_user_token(user_id,
                                   'playlist-read-collaborative',
                                   client_id,
                                   client_secret,
                                   redirect_uri='https://www.facebook.com/groups/1223037501082162')