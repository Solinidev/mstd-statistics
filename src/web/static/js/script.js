function el(idName) {
    return document.getElementById(idName).textContent;
}

function perc_divide(str) {
    return str.split('%');
}

function add_enter(arr, host) {
    let str = '타임라인 지분 측정기\n\n';
    for (var i = 0; i < arr.length; i++) {
        if (i == arr.length - 2) {
            str += arr[i] + '%\n\n';
            continue;
        }
        str += arr[i] + '%\n';
    }
    str2 = str.slice(0, -2) + host;
    return str2;
}

function toot(instance) {
    let text = el('result').trim();
    let text2 = add_enter(perc_divide(text), host);
    window.open(instance + '/share?text=' + encodeURIComponent(text2));
}