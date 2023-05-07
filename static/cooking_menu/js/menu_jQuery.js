$(function(){
//以下を写しただけ。わかりやすくて良かった。
  //https://www.omakase.net/blog/2021/12/accordionmenu.html

/*
  //クリックで動く
  $('.nav-open').click(function(){
    $(this).toggleClass('active');
    $(this).next('nav').slideToggle();
  });
*/

/*
  //確かに動くけど、カーソル当てると非表示になっちゃう。。。
  //ホバーで動く
  $('.nav-open').hover(function(){
    $(this).toggleClass('active');
    $(this).next('nav').slideToggle();
  });
*/


  //フェードイン・フェードアウト版
  //クリックで動く
  $('.nav-open').click(function(){
    if($(this).hasClass('active')){
      $(this).toggleClass('active');
      $(this).next('nav').fadeOut();
    } else {
      $(this).toggleClass('active');
      $(this).next('nav').fadeIn();
    }
  });


/*
  //フェードイン・フェードアウト版
  //確かに動くけど、カーソル当てると非表示になっちゃう。。。
  //ホバーで動く
  $('.nav-open').hover(function(){
    $(this).toggleClass('active');
    $(this).next('nav').fadeIn();
  },
  function() {
    $(this).toggleClass('active');
    $(this).next('nav').fadeOut();
  });
*/

});