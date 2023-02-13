var ctx,img,point;
var yields = {"imgSrcList":[],"imgPointList":{}};

$(document).ready(function() {
    $("img").click(function(){
        $("img").removeClass("img-selected");
        $(this).addClass("img-selected");
        
        var imgCanvas = document.getElementById("imgCanvas");
        ctx = imgCanvas.getContext("2d");
        img = this;
        ctx.beginPath();
        ctx.drawImage(img, 0, 0, imgCanvas.width, imgCanvas.height);
        $('#imageModal').modal('show');
    });

    $("#imgCanvas").on("mousedown", function (e) {
        point = getMousePosition(imgCanvas, e);
    });

    $("#btnNext1").click(function(){
        let imgSrc = $(".img-selected").attr("src");
        if (imgSrc && point){
            yields.imgSrcList.push(imgSrc);
            yields.imgPointList.x1 = point[0];
            yields.imgPointList.y1 = point[1];
            point = null;
            $("img").removeClass("img-selected");
            $("#divSet1").hide();
            $("#divSet2").show();
        }else{
            alert("Please Select Image Point");
        }
    });

    $("#btnNext2").click(function(){
        let imgSrc = $(".img-selected").attr("src");
        if (imgSrc && point){
            yields.imgSrcList.push(imgSrc);
            yields.imgPointList.x2 = point[0];
            yields.imgPointList.y2 = point[1];
            point = null;
            $("img").removeClass("img-selected");
            $("#divSet2").hide();
            $("#divSet3").show();
        }else{
            alert("Please Select Image Point");
        }
    });
    
});

function validateForm(){
    let imgSrc = $(".img-selected").attr("src");
    if (imgSrc && point){
        yields.imgSrcList.push(imgSrc);
        yields.imgPointList.x3 = point[0];
        yields.imgPointList.y3 = point[1];
        point = null;
        $('input[name=yields]').val(JSON.stringify(yields));
        return true;
    }else{
        alert("Please Select Image Point");
        return false;
    }
}

function getMousePosition(canvas, event) {
    let rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;

    var posx = parseInt(x);
    var posy = parseInt(y);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    ctx.arc(posx, posy, 20, 0, 2 * Math.PI);
    ctx.lineWidth = "5";
    ctx.strokeStyle = "red";
    ctx.stroke();

    return [posx,posy]
  }