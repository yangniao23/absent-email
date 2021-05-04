const isabsent = document.querySelectorAll(".isabsent");
const sendmail = document.querySelector('.exec');
const username = document.querySelector('.username');
const logout = document.querySelector('.logout');

async function postData(url = '', data = {}) {
	// 既定のオプションには * が付いています
	const response = await fetch(url, {
	  method: 'POST', // *GET, POST, PUT, DELETE, etc.
	  mode: 'cors', // no-cors, *cors, same-origin
	  cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
	  credentials: 'same-origin', // include, *same-origin, omit
	  headers: {
		'Content-Type': 'application/json'
		// 'Content-Type': 'application/x-www-form-urlencoded',
	  },
	  redirect: 'follow', // manual, *follow, error
	  referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
	  body: JSON.stringify(data) // 本文のデータ型は "Content-Type" ヘッダーと一致する必要があります
	})
	return response.json(); // レスポンスの JSON を解析
}

/*
isabsent.forEach((i) => {
	i.addEventListener("change", () => {
			console.log(i.value);
	});
});
*/

sendmail.addEventListener('click', e => {
	const data = [];
	
	isabsent.forEach(i => {
		if(i.checked) data.push(Number(i.value));
	})
	
	const confirm_text = (data.length === 0)? "今日の欠席者はなしでよろしいですか？": "今日の欠席者は" + data.map(i => String(i) + '番') + "でよろしいですか？";
	
	if( confirm(confirm_text) ) {
		postData('api', {"token":"OT8M$DH8AzEmN#1oRS2ZGHXJR", "numlist":data}).then(value => {
			console.log(value);
			if(value.status === "200") alert("正常に送信されました．");
			else alert("正常に送信されませんでした．\n" + JSON.stringify(value));
		});
	}
});