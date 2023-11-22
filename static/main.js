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
        fetch("/get_vendors", {
            method: "POST",
            body: new URLSearchParams({
                departmentCode: document.querySelector("#select_dept").value,
            })
        }).then((result) => {
            return result.json();
        }).then((json) => {
            const select = document.querySelector("#select_vendor")
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
            option.value = "";
            select.append(option);
            for (let key in optionData) {
                const option = document.createElement("option");
                option.text = optionData[key];
                option.value = key;
                select.append(option);

            }
        })
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
        fetch("/regist", {
            method: "POST",
            body: new URLSearchParams({
                year: document.querySelector("#year").value,
                month: document.querySelector("#month").value,
                select_dept: document.querySelector("#select_dept").value,
                select_vendor: document.querySelector("#select_vendor").value,
                select_resource: document.querySelector("#select_resource").value,
                working_hours: document.querySelector("#working_hours").value,
                others: document.querySelector("#others").value,
                remarks: document.querySelector("#remarks").value,
            })
        }).then((result) => {
            return result.json();
        }).then((json) => {
            target = document.querySelector("#table_area")
            generate_table(target, json.history)
        })
        document.querySelector("#select_resource").value = "";
        document.querySelector("#keyword_name").value = "";
        document.querySelector("#working_hours").value = "";
        document.querySelector("#others").value = "";
        document.querySelector("#remarks").value = "";
        const keyword = select_vendor.value;
        get_menu(keyword, select_resource, "/get_resources");
    })

    // 入力履歴のテーブルを作成
    function generate_table(_table, _data) {
        clear_table(_table)
        let firstTime = true;
        const _thead = document.createElement("thead");
        const _tbody = document.createElement("tbody");
        _data.forEach((_row) => {
            const _table_row = document.createElement("tr");
            if (firstTime) {
                _row.forEach((_column) => {
                    const _cell = document.createElement("th");
                    _cell.innerHTML = _column
                    _table_row.appendChild(_cell);
                })
                firstTime = false;
                _thead.append(_table_row);
            } else {
                _row.forEach((_column) => {
                    const _cell = document.createElement("td");
                    _cell.innerHTML = _column
                    _table_row.appendChild(_cell);
                })
                _tbody.append(_table_row);
            }
        })
        _table.append(_thead);
        _table.append(_tbody);
    }

    // 前回取得したテーブルのデータを削除
    function clear_table(_table) {
        while (_table.rows.length !== 0) {
            _table.deleteRow(_table.rows.length - 1);
        }
    }
}
