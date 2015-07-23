 $(document).ready(function() {
    $(".droppable").sortable({
      update: function( event, ui ) {
        Dropped();
      }
    });    
  });
    
  function Dropped(event, ui){
    $(".draggable").each(function(){
        console.log('Dropped: $(this).html() = ', $(this).html());
    });
  }        