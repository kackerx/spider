 eval(function (d, f, a, c, b, e) {
     b = function (a) {
         return a.toString(f)
     };
     if (!"".replace(/^/, String)) {
         for (; a--;) e[b(a)] = c[a] || b(a);
         c = [function (a) {
             return e[a]
         }];
         b = function () {
             return "\\w+"
         };
         a = 1
     }
     for (; a--;) c[a] && (d = d.replace(new RegExp("\\b" + b(a) + "\\b", "g"), c[a]));
     return d
 }("1 2=c.3('8');4.b(2,'5',{6:7(){1 a=\"\";9(1 i=0;i<d;i++){a=a+i.e();f.g(0,0,a)}}});h.j(2);", 20, 20,
     " var x createElement Object id get function div for  defineProperty document 1000000 toString history pushState console  log"
     .split(' '), 0, {}));