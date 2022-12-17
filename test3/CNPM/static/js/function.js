
function addToCart() {
    fetch('/api/tuyen-bay', {
        method: "post",
        body: JSON.stringify({
            "di": changeFunc1(),
            "den": changeFunc2()
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    alert('CC')
//    alert(changeFunc1())
//    alert(changeFunc2())

}



function changeFunc1() {
    var selectBox = document.getElementById("diem_di");
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;
    return(selectedValue);
}

function changeFunc2() {
    var selectBox = document.getElementById("diem_den");
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;
    return(selectedValue);
}
