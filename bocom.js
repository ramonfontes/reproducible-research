'use strict'

const rp = require('request-promise')

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
 }

const data = {
  email: `dosalunuyul+${makeid(5)}@emailnyagantilahtolol.net`,
  password: 'JanganZinaBang'
}


const request = rp.defaults({
  baseUrl: 'https://iphone-xml.booking.com/json/',
  json: true,
  qs: {
    user_os: '8.0.0',
    user_version: '22.9-android',
    device_id: 'f0ab31ce-a92b-4ffd-a28b-e7897d22d799',
    network_type: 'wifi',
    languagecode: 'en-us',
    display: 'normal_xxhdpi',
    affiliate_id: 337862
  },
  headers: {
    'X-LIBRARY': 'okhttp+network-api',
    'Authorization': 'Basic dGhlc2FpbnRzYnY6ZGdDVnlhcXZCeGdN',
    'User-Agent': 'Booking.App/22.9 Android/8.0.0; Type: mobile; AppStore: google; Brand: google; Model: Android 8.0.0; SM-G960F Build/R16NW',
    'X-Booking-API-Version' :'1'
  }
})

const hotels = ['3326463', '4984319']
async function main () {
  const register = await request('mobile.createUserAccount', {
    method: 'POST',
    body: { ...data, return_auth_token: 1 }
  })
//   console.log(register)
console.log(`[+] Register Success | ${data.email}:${data.password}`)

  const createWishList = await request('mobile.Wishlist', {
    qs: {
      wishlist_action: 'create_new_wishlist',
      auth_token: register.auth_token,
      name: 'Jakarta',
      hotel_id: '28250'
    }
  })
//   createWishList.success
  console.log(`[+] Claim`)
  for (const id of hotels) {
    const saveWishList = await request('mobile.Wishlist', {
      qs: {
        'wishlist_action': 'save_hotel_to_wishlists',
        'list_ids': createWishList.id,
        'new_states': 1,
        'hotel_id': id,
        'list_dest_id': 'city%3A%3A-2679652',
        'update_list_search_config': 1,
        'checkin': '2020-06-27',
        'checkout': '2020-06-28',
        'num_rooms': 1,
        'num_adults': 2,
        'num_children': 0,
        auth_token: register.auth_token
      }
    })
    if (saveWishList.gta_add_three_items_campaign_status.status !== 'not_yet_reached_wishlist_threshold') {
        console.log(saveWishList.gta_add_three_items_campaign_status.modal_body_text, saveWishList.gta_add_three_items_campaign_status.modal_header_text)
    } 
  }
}

main()