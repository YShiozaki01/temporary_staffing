document.addEventListener('DOMContentLoaded',pageLoad)

// ページをロードした時にテキストボックスにリスナを登録
function pageLoad() {
    const keyword = document.querySelector("#keyword");
    textbox.addEventListener('keydown', enterKeyPress);
}

// テキストボックスでEnterキーが押されたらコンソールに文字を表示
function enterKeyPress(event) {
    if (event.key === "Enter") {
        function () {
            //formオブジェクトを取得する
            var form1 = document.querySelector("form1");
            //Submit形式指定する（post/get）
            form.method = "post";
            //action先を指定する
            form.action = "/register";          
            //Submit実行
            fm.submit();
          }
    }
}