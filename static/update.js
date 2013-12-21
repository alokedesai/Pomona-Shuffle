function update() {
      $(function(){
      
      var $container = $('.deck');
      
      // // add randomish size classes
      // $container.isotope('reLayout');
      
      $container.isotope({
        itemSelector: '.card',
        masonry : {
          columnWidth : 1
        }
      });
      
     
      
      //change size of clicked element
      $container.delegate( '.card', 'click', function(){
        $(this).closest(".card").toggleClass('large');
        $container.isotope('reLayout');
      });

      $("div.card:first").delay(8000).trigger("click")
      
      });

 keyNavigationDisabled = false;
          
  }

