function update() {
      var $container = $('#container');
    
    
      // add randomish size classes
      $container.find('.card').each(function(){
        var $this = $(this);
          $this.addClass('width2');
          $this.addClass('height2');
          $this.find('h3,p').hide();
        });
      $container.isotope({
      
      itemSelector : '.card',
      masonry : {
        columnWidth : 120
      },
      masonryHorizontal : {
        rowHeight: 120
      },
      getSortData : {
        symbol : function( $elem ) {
          return $elem.attr('data-symbol');
        },
        category : function( $elem ) {
          return $elem.attr('data-category');
        },
        number : function( $elem ) {
          return parseInt( $elem.find('.cardNumber').text(), 10 );
        },
        weight : function( $elem ) {

          return $elem.css('background');
        },
        name : function ( $elem ) {
          return $elem.find('.classTitle').text();
        }
      }
    });
    
      var $optionSets = $('#options .option-set'),
          $optionLinks = $optionSets.find('a');

      $optionLinks.click(function(){
        var $this = $(this);
        // don't proceed if already selected
        if ( $this.hasClass('selected') ) {
          return false;
        }
        var $optionSet = $this.parents('.option-set');
        $optionSet.find('.selected').removeClass('selected');
        $this.addClass('selected');
  
        // make option object dynamically, i.e. { filter: '.my-filter-class' }
        var options = {},
            key = $optionSet.attr('data-option-key'),
            value = $this.attr('data-option-value');
        // parse 'false' as false boolean
        value = value === 'false' ? false : value;
        options[ key ] = value;
        if ( key === 'layoutMode' && typeof changeLayoutMode === 'function' ) {
          // changes in layout modes need extra logic
          changeLayoutMode( $this, options )
        } else {
          // otherwise, apply new options
          $container.isotope( options );
        }
        
        return false;
      });


    
      // change layout
      var isHorizontal = false;
      function changeLayoutMode( $link, options ) {
        var wasHorizontal = isHorizontal;
        isHorizontal = $link.hasClass('horizontal');

        if ( wasHorizontal !== isHorizontal ) {
          // orientation change
          // need to do some clean up for transitions and sizes
          var style = isHorizontal ? 
            { height: '80%', width: $container.width() } : 
            { width: 'auto' };
          // stop any animation on container height / width
          $container.filter(':animated').stop();
          // disable transition, apply revised style
          $container.addClass('no-transition').css( style );
          setTimeout(function(){
            $container.removeClass('no-transition').isotope( options );
          }, 100 )
        } else {
          $container.isotope( options );
        }
      }


    
      // change size of clicked element
      

      // toggle variable sizes of all elements
      $('#toggle-sizes').find('a').click(function(){
        $container
          .toggleClass('variable-sizes')
          .isotope('reLayout');
        return false;
      });


    
      $('#insert a').click(function(){
        var $newEls = $( fakeElement.getGroup() );
        $container.isotope( 'insert', $newEls );

        return false;
      });

      $('#append a').click(function(){
        var $newEls = $( fakeElement.getGroup() );
        $container.append( $newEls ).isotope( 'appended', $newEls );

        return false;
      });


    var $sortBy = $('#sort-by');
    $('#shuffle a').click(function(){
      $container.isotope('shuffle');
      $sortBy.find('.selected').removeClass('selected');
      $sortBy.find('[data-option-value="random"]').addClass('selected');
      return false;
    });

    $container.delegate( '.card', 'click', function(){
        var swap = $(this).find('.cardNumber').text();
        if((swap === '6' && $(this).hasClass('large'))||$('.card').is(':animated')){

        }
        else{
        var $oldItem = $container.find('.focus');  
        $oldItem.find('.cardNumber').text(swap);      
        $oldItem.toggleClass('focus');
        $container.find('.large').find('h3,p').hide();
        $container.find('.large').find('.classTitle').css({'font-size':'1.5em','font-weight':'none'});
        $container.find('.large').toggleClass('large');
        var $removable = $(this);
        $removable.find('.cardNumber').text('6');
        if(swap>6){
          $oldItem.hide();
          var $oldClone = $oldItem.stop().clone();
          $oldClone.css('display','inline').delay();
          $container.isotope('remove',$oldItem);
          $container.isotope('insert',$oldClone);
        }        
        $removable.hide();
        $removable.toggleClass('large');
        $removable.toggleClass('focus');
        $removable.find('.classTitle').css({'font-size':'2.5em','font-weight':'bold'});
        $removable.find('h3,p').show();
        var $newItem = $removable.clone();
        $newItem.css('display','inline');
        $container.isotope('remove',$removable);
        $container.isotope('insert',$newItem);

        
        $container.isotope({sortBy: 'number'});
        
        $container.isotope('reLayout');
      }
      });
          
  }
