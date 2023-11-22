const array = [
    ["ID", "請求年", "請求月", "部門", "会社", "人材", "作業時間", "その他", "備考"],
    [1492, 2023, 9, '12', 28, 359, 48.0, '', ''],
    [1493, 2023, 9, '12', 28, 360, 205.0, '', ''],
    [1494, 2023, 9, '12', 28, 786, 112.75, '', ''],
    [1495, 2023, 9, '12', 29, 361, 0.0, '162181', ''],
    [1496, 2023, 9, '12', 29, 362, 0.0, '165654', ''],
    [1497, 2023, 9, '12', 29, 363, 0.0, '173923', ''],
    [1498, 2023, 9, '12', 29, 364, 0.0, '174', ''],
    [1499, 2023, 9, '12', 29, 365, 0.0, '4418', ''],
    [1500, 2023, 9, '12', 29, 367, 0.0, '360000円', '']
]

target = document.querySelector("#table_area")
generate_table(target, array)

// function generate_table(_table, _data) {
//     const _tbody = document.createElement("tbody");
//     _data.forEach((_row) => {
//         const _table_row = document.createElement("tr");
//         _row.forEach((_column) => {
//             const _cell = document.createElement("td");
//             _cell.innerHTML = _column
//             _table_row.appendChild(_cell);
//         })
//         _tbody.append(_table_row);
//     })
//     _table.append(_tbody);
// }

function generate_table(_table, _data) {
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
        } else {
            _row.forEach((_column) => {
                const _cell = document.createElement("td");
                _cell.innerHTML = _column
                _table_row.appendChild(_cell);
            })
        }
        _tbody.append(_table_row);
    })
    _table.append(_tbody);
}
