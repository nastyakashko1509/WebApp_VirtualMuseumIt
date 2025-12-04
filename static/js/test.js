let name = "Cat";

function sayHi() {
    console.log(name);
}

setTimeout(function() {
    let name = "Dog";
    sayHi();
}, 1000);

let ar = ["a", "b", "c"]; 
ar.push(function(){console.log(this);})
ar[4]();

console.log(0 || 1 && 0 || 3);

var o = new Array(1, 2), u = new Array(3);
console.log(o[0] + u[0]);

let x = 4;
console.log( x+++1 );
console.log( x++ );

var w = ( "a", "b" )
var w1 = new Array("a", "b")
var w2 = [ "a", "b" ]
let w3 = "a, b".split(",")
console.log(w)
console.log(w1)
console.log(w2)
console.log(w3)

var a = 3;
var b = {toString:function(){return 5}};  
var c = 3;
console.log(a + b + c); 

console.log(true + false + "1"[0]);

f.call(f);
function f() {
    console.log( this ); // alert нужно
}

console.log(parseInt("-1.2"))
console.log(parseInt("1px"))
console.log(parseInt("$1.2"))
console.log(parseInt("0 минут"))

var arr = new Array();
arr[arr.length] = 0;
arr[arr.length] = 1;
console.log(arr.length);

let n = (2, 3-1, 1) * 2;
console.log(n);

let obj = {
    go: function() { console.log(this) }
};
(obj.go)()

console.log(10e-1['toString'](10));

console.log([] + false - null + true);
