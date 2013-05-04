var colorDiff = new function () {
    var colorID = 0,
        radius = 0,
        dir = '',
        isCloser = [],

        dirs = {'a': [0, -1], 'b': [1, 0], 'c': [0, 1], 'd': [-1, 0]},
        url = '../py/measurement.py',
        elem1 = null,
        elem2 = null,
        refelem=null;

    function update(data){
        console.log(data);
        colorID  =data.color_id;
        radius = data.radius;
        dir = data.direction;
        var colorInt = parseInt('0x'+data.hex.substr(-6)),
            r=(colorInt>>16)&0xff,
            g=(colorInt>>8)&0xff,
            b=colorInt&0xff,
            refColor= hexColor(r+dirs[data.refdir][0]*radius,g,b+dirs[data.refdir][1]*radius),
            compColor=  hexColor(r+dirs[dir][0]*radius+dirs[dir][0]*data.offset,g,b+dirs[dir][1]*radius+dirs[dir][1]*data.offset);
           console.log(refColor+", "+compColor);
         refelem.style.backgroundColor='#'+data.hex;
        if(Math.random()<.5){
            elem1.style.backgroundColor=refColor;
            elem2.style.backgroundColor=compColor;
            isCloser = [false,true];

        }
        else {
            elem1.style.backgroundColor=compColor;
            elem2.style.backgroundColor=refColor;
            isCloser=[true,false];

        }

        $('#colors').removeClass().addClass('visible');
        function hexColor(ri,gi,bi){
            function hex(num){
                return ('00'+num.toString(16)).substr(-2);
            }
            return '#'+hex(ri)+hex(gi)+hex(bi);
        }

    }
    this.init = function (el1, el2,refel) {
        elem1 = el1;
        elem2 = el2;
        refelem=refel;
        console.log(el1);
        $.ajax({
             url:url,
              type:'POST',
              data:{
                  action:'get'
              },
            success:  function(data){
                update(data)
            }
        })

    }

    this.sendColors = function (num) {
        $('#colors').removeClass().addClass('invisible');
        $.ajax({
            url:url,
            type:'POST',
            data:{
                action:'save',
                colorID:colorID,
                radius:radius,
                dir:dir,
                isCloser:isCloser[num]
            } ,
            success:function(data){
                update(data)}

        })
    }


}
colorDiff.init($('#col1')[0],$('#col2')[0],$('#refcol')[0]);

$('#col1').on('click', function () {
    colorDiff.sendColors(0)
});
$('#col2').on('click', function () {
    colorDiff.sendColors(1)
});