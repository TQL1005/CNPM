function addData(id, name, price, so_luot_bay, tong_doanh_thu, ty_le) {
     fetch('/api/data', {
        method: "POST",
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
            'so_luot_bay': so_luot_bay,
            'ty_le': ty_le,
            'tong_doanh_thu': tong_doanh_thu,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
     }).then(res => res.json()).then(data => {
        console.info(data)
        })
}
function deleteData() {
     fetch('/api/data', {
        method: "delete",
     }).catch(err => console.info(err))
}