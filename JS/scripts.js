$(document).ready(function() {
  // 记录初始宽度，用于后续计算宽度变化时使用
  var initialLeftSectionWidth = null;
  var initialRightSectionWidth = null;
  var initialPageWidth = $(window).width();

  $(window).resize(function() {
    // 当窗口大小改变时，重新初始化初始宽度记录变量
    initialLeftSectionWidth = null;
    initialRightSectionWidth = null;
  });

  // 点击显示左下方部分的按钮
  $('.show-lower-left-btn').click(function() {
    $('.requirement-description').show();
    $('.mathematical-modeling').show();
    // 获取页面可视区域高度
    var viewportHeight = $(window).height() * 0.9;
    // 去除上下边框的高度（这里假设边框宽度都是1px，可根据实际修改）
    var availableHeight = viewportHeight - 2;
    // 初始分配给上下两个框各一半高度
    var upperInitialHeight = availableHeight * 0.30;
    var lowerInitialHeight = availableHeight * 0.70;
    $('.requirement-description').height(upperInitialHeight);
    $('.mathematical-modeling').height(lowerInitialHeight);
    // 记录初始位置，用于后续计算拖动偏移量
    var startY = null;

    
     // 记录鼠标是否在拖动操作中（在拉伸条按下鼠标后开始拖动为true），初始化为false
     var isDragging = false;

     // 定义一个容差范围，用于判断鼠标在稍微离开拉伸条区域时仍能继续拖动，单位为像素，可根据实际情况调整
     var tolerance = 5; 

     // 绑定鼠标进入和离开事件，用于标记鼠标是否进入拉伸条区域附近（考虑容差范围）
     $('.requirement-description').on('mouseenter', function() {
         var rect = this.getBoundingClientRect();
         $(this).data('borderTop', rect.bottom - 2 - tolerance);
         $(this).data('borderBottom', rect.bottom + tolerance);
     }).on('mouseleave', function() {
         $(this).removeData('borderTop');
         $(this).removeData('borderBottom');
         if (!isDragging) {
             isDragging = false;
         }
     });

     $('.mathematical-modeling').on('mouseenter', function() {
         var rect = this.getBoundingClientRect();
         $(this).data('borderTop', rect.top - tolerance);
         $(this).data('borderBottom', rect.top + 2 + tolerance);
     }).on('mouseleave', function() {
         $(this).removeData('borderTop');
         $(this).removeData('borderBottom');
         if (!isDragging) {
             isDragging = false;
         }
     });

     // 全局鼠标移动事件处理，用于处理拖动逻辑，考虑容差范围让拖动更流畅
     $(document).on('mousemove', function(e) {
         if (isDragging && startY!== null) {
             var offsetY = e.pageY - startY;
             var upperHeight = $('.requirement-description').height();
             var lowerHeight = $('.mathematical-modeling').height();
             // 计算新的高度，限制最小和最大高度，避免出现不合理的布局
             var newUpperHeight = Math.max(100, Math.min(upperHeight + offsetY, availableHeight - 100));
             var newLowerHeight = Math.max(100, Math.min(lowerHeight - offsetY, availableHeight - 100));
             $('.requirement-description').height(newUpperHeight);
             $('.mathematical-modeling').height(newLowerHeight);
             startY = e.pageY;
         }
     });

     // 绑定鼠标按下事件，用于记录初始位置和判断是否在拉伸条区域（考虑容差范围）按下鼠标并开始拖动
     $('.requirement-description').on('mousedown', function(e) {
         var rect = this.getBoundingClientRect();
         if (e.pageY >= rect.bottom - 2 - tolerance && e.pageY <= rect.bottom + tolerance) {
             startY = e.pageY;
             isDragging = true;
         }
     });

     $('.mathematical-modeling').on('mousedown', function(e) {
         var rect = this.getBoundingClientRect();
         if (e.pageY >= rect.top - tolerance && e.pageY <= rect.top + 2 + tolerance) {
             startY = e.pageY;
             isDragging = true;
         }
     });

     // 绑定鼠标抬起事件，用于重置相关状态
     $(document).on('mouseup', function() {
         startY = null;
         isDragging = false;
     });
 });

    



// 点击显示右侧部分的按钮
$('.show-right-btn').click(function() {
  $('.right-section').show();
  // 记录鼠标是否在右侧区域拉伸条内进行水平拖动操作，初始化为false
  var isDraggingHorizontal = false;
  // 记录水平拖动的初始位置（横坐标），初始化为null
  var startX = null;
  // 定义水平拖动的容差范围，用于判断鼠标在稍微离开拉伸条区域时仍能继续水平拖动，单位为像素，可根据实际情况调整
  var horizontalTolerance = 5;
  // 用于节流的定时器变量，控制鼠标移动事件的触发频率
  var horizontalMoveTimer = null;

  $('.right-section').resizable({
      handles: "w", // 只通过左边沿（w）进行拖动，实现右边固定，左边可调整宽度
      grid: [10, 0], // 水平方向移动步长为10px
      minWidth: 600, // 最小宽度限制
      maxWidth: 900, // 最大宽度限制，可根据实际调整
      resize: function(event, ui) {
          // 获取左侧区域（包含上下两个框）的总宽度
          var leftSection = $('.left-section');
          var leftSectionWidth = leftSection.width();
          // 获取右侧框当前宽度
          var rightSectionWidth = $('.right-section').width();

          // 如果是首次记录初始宽度或者窗口大小改变后（此时这两个变量被重置为null）
          if (initialLeftSectionWidth === null || initialRightSectionWidth == null) {
              initialLeftSectionWidth = leftSectionWidth;
              initialRightSectionWidth = rightSectionWidth;
          }

          // 计算宽度变化量
          var widthDelta = ui.size.width - initialRightSectionWidth;

          // 根据宽度变化量等比例调整左侧区域的宽度，同时保持右侧框右侧边框固定
          var newLeftSectionWidth = initialLeftSectionWidth - widthDelta;
          leftSection.width(newLeftSectionWidth);

          // 更新右侧框的宽度，保持右侧边框位置固定
          $('.right-section').css({
              width: ui.size.width,
              left: 0
          });

          // 解决内容溢出问题，先获取右侧框内所有元素
          var elements = $('.right-section').find('*');
          // 遍历每个元素，更新其宽度、左边距和右边距，确保内容不溢出且布局合理
          elements.each(function() {
              var element = $(this);
              var elementWidth = element.width();
              var newWidth = ui.size.width - element.position().left - element.position().right - 20;
              element.css({
                  'width': newWidth,
                  'margin-left': element.position().left,
                  'margin-right': ui.size.width - element.position().left - newWidth
              });
          });
      }
  });

  // 绑定鼠标进入和离开事件，用于判断鼠标是否进入右侧区域拉伸条（考虑水平容差范围）
  $('.right-section').on('mouseenter', function() {
      var rect = this.getBoundingClientRect();
      $(this).data('borderLeft', rect.left - horizontalTolerance);
      $(this).data('borderRight', rect.left + 2 + horizontalTolerance);
  }).on('mouseleave', function() {
      $(this).removeData('borderLeft');
      $(this).removeData('borderRight');
      if (!isDraggingHorizontal) {
          isDraggingHorizontal = false;
      }
  });

  // 全局鼠标移动事件处理，用于处理水平拖动逻辑，使用节流优化，考虑水平容差范围让拖动更流畅
  $(document).on('mousemove', function(e) {
      if (isDraggingHorizontal && startX!== null) {
          if (!horizontalMoveTimer) {
              var offsetX = e.pageX - startX;
              var rightSectionWidth = $('.right-section').width();
              var leftSection = $('.left-section');
              var leftSectionWidth = leftSection.width();
              // 计算新的右侧框宽度，限制最小和最大宽度，避免出现不合理的布局
              var newRightSectionWidth =rightSectionWidth - offsetX;
              var widthDelta = rightSectionWidth - newRightSectionWidth;
              var newLeftSectionWidth = leftSectionWidth + widthDelta;
              leftSection.width(newLeftSectionWidth);
              $('.right-section').width(newRightSectionWidth);
              startX = e.pageX;
              horizontalMoveTimer = setTimeout(() => {
                  horizontalMoveTimer = null;
              }, 16); // 每16毫秒（约60帧每秒）更新一次，可根据实际情况调整
          }
      }
  });

  // 绑定鼠标按下事件，用于记录初始位置和判断是否在右侧区域拉伸条按下鼠标并开始水平拖动
  $('.right-section').on('mousedown', function(e) {
      var rect = this.getBoundingClientRect();
      if (e.pageX >= rect.left - horizontalTolerance && e.pageX <= rect.left + 2 + horizontalTolerance) {
          startX = e.pageX;
          isDraggingHorizontal = true;
      }
  });

  // 绑定鼠标抬起事件，用于重置水平拖动相关状态
  $(document).on('mouseup', function() {
      startX = null;
      isDraggingHorizontal = false;
  });
});
});


  
  

  
  
  
  