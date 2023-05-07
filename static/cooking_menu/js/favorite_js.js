$(function() {
  //チェックボックスが切り替わったら発動
  $('input[name="favorite_flag"]').on('change', function () {
    var val = $(this).val();
    var favorite_flag = false;
    if ($(this).prop('checked')) {
      favorite_flag = true;
    }
    $.ajax({
//      JSファイルが静的ファイルなので、Djangoテンプレートが使用できない？！
//      url: '{% url "favorite_js" %}',
      url: 'http://localhost:8000/cooking_menu/favorite_js',
      type: 'POST',
      //dataType:'json',     //data type script・xmlDocument・jsonなど
      data:{
        'value_id':val,
        'value_favorite_flag':favorite_flag,
        'csrftoken':csrftoken,
      },
    }).done(function(data) { 
      //console.log('成功');
    }).fail(function(XMLHttpRequest, textStatus, errorThrown){
      //console.log(XMLHttpRequest.status);
      //console.log(textStatus);
      //console.log(errorThrown);
    });
  });  
});