{

    function get_menu(keyword, select, route) {
        const formData = new FormData;
        formData.append("keyword", keyword);
        fetch(route, {
            method: "POST",
            body: formData,
        }).then(function (result) {
            return result.json();
        }).then(function (json) {
            // 前回のオプション要素をクリア
            let len = select.length;
            for (let i = 0; i < len; i++) {
                select.remove(0);
            }
            // セレクトボックスのオプション要素を作成する
            const optionData = JSON.parse(JSON.stringify(json));
            const option = document.createElement("option");
            // 選択先頭
            option.text = "--選択--";
            option.value = 0;
            select.append(option);
            for (let key in optionData) {
                const option = document.createElement("option");
                option.text = optionData[key];
                option.value = key;
                select.append(option);

            }
        });
    }

    // 部門が選択されたら、業者のメニューデータを取得
    const select_dept = document.querySelector("#select_dept");
    const select_vendor = document.querySelector("#select_vendor");
    select_dept.addEventListener("change", () => {
            const keyword = select_dept.value;
            get_menu(keyword, select_vendor, "/get_vendors");
    });

    // 業者が選択されたら、人材のメニューデータを取得
    const select_resource = document.querySelector("#select_resource");
    select_vendor.addEventListener("change", () => {
            const keyword = select_vendor.value;
            get_menu(keyword, select_resource, "/get_resources");
    });

    // 人材名の一部が入力されたらさらに絞り込み
    const input_name = document.querySelector("#keyword_name");
    input_name.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            const keywordZero = select_vendor.value;
            const keywordOne = input_name.value;
            const keywords = {}
            keywords.key1 = keywordZero
            keywords.key2 = keywordOne
            kwJson = JSON.   stringify(keywords)
            get_menu(kwJson, select_resource, "/get_resources_name");
        }
    })

    // 作業時間欄にプラス記号が含まれていたら、足し算
    const workingHours = document.querySelector("#working_hours");
    workingHours.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            if (workingHours.value.includes("+") === true) {
                const hours = workingHours.value.split("+");
                let result = 0;
                for (i = 0; i < hours.length; i++) {
                    result += parseFloat(hours[i]);
                }
                workingHours.value = result;
            }
        }
    });

    // フォーム送信
    document.querySelector("#button").addEventListener("click", () => {
        document.form01.submit();
    })


}