def test_get_info(client, create_user_owner, owner_token):
    response = client.get('/api/user/get_info', headers={'Authorization': f'Bearer {owner_token}'})

    assert response.status_code == 200
    data = response.get_json()['data']

    # Assertions for user information
    assert 'type' in data and data['type'] == 'users'
    assert 'id' in data and data['id'] == create_user_owner.user_id
    assert 'attributes' in data \
           and 'username' in data['attributes'] \
           and data['attributes']['username'] == create_user_owner.username

    # Assertions for account information
    assert 'relationships' in data and 'account' in data['relationships']
    account_data = data['relationships']['account']['data']
    assert 'type' in account_data and account_data['type'] == 'accounts'
    assert 'id' in account_data and account_data['id'] == create_user_owner.account_id


def test_get_info_unauthorized(client):
    response = client.get('/api/user/get_info')
    assert response.status_code == 401
