$(document).ready(function() {
  // Remove Items From Cart
  $('a.remove').click(function(event) {
    event.preventDefault();
    var basketItem = $(this).closest('.cart-item');
    var basketId = basketItem.data('basket-id');
    removeBasketItem(basketId, basketItem);
  });

  // Just for testing, show all items
  $('a.btn.continue').click(function(event) {
    event.preventDefault();
    $('li.cart-item').show(400);
  });

  // Обрабатываем событие изменения значения ползунка
  $('.update-quantity').change(function() {
    var quantity = parseInt($(this).val());
    var basketId = $(this).data('basket-id');
    updateBasketQuantity(basketId, quantity);
  });

  // Функция для получения значения cookie по имени
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Функция для удаления блюда из корзины
  function removeBasketItem(basketId, basketItem) {
    // Получите CSRF-токен из cookies
    var csrftoken = getCookie('csrftoken');

    // Установите CSRF-токен в заголовке запроса
    $.ajaxSetup({
      headers: { "X-CSRFToken": csrftoken }
    });

    // Отправляем AJAX-запрос на сервер, чтобы удалить блюдо из корзины
    $.ajax({
      url: '/basket_remove/' + basketId + '/',
      method: 'POST',
      success: function(response) {
        // Если запрос успешен, скрываем удаленное блюдо на странице
        basketItem.hide(400);
      },
      error: function(xhr, status, error) {
        // Обрабатываем ошибку при удалении блюда
        console.error(error);
      }
    });
  }

  // Функция для обновления количества блюд в корзине
  function updateBasketQuantity(basketId, quantity) {
    // Получите CSRF-токен из cookies
    var csrftoken = getCookie('csrftoken');

    // Установите CSRF-токен в заголовке запроса
    $.ajaxSetup({
      headers: { "X-CSRFToken": csrftoken }
    });

    // Отправляем AJAX-запрос на сервер, чтобы обновить количество блюд
    $.ajax({
      url: '/update_basket_quantity/' + basketId + '/',
      method: 'POST',
      data: { quantity: quantity },
      success: function(response) {
        // Если запрос успешен, обновляем только необходимые элементы на странице
        if (response.total_price_sum !== undefined) {
          var totalPriceElement = $('.total-row.final .value.total-price');
          totalPriceElement.text(response.total_price_sum.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0}) + ' руб.');
        }
        if (response.total_price_item !== undefined) {
          var basketItem = $('.cart-item[data-basket-id="' + basketId + '"]');
          var itemPriceElement = basketItem.find('.item-price.item-price-' + basketId);
          itemPriceElement.text(response.total_price_item.toLocaleString() + ' руб.');
        }
        // Обновляем значение "Total quantity"
        var totalQuantityElement = $('.total-row .value.total-quantity');
        totalQuantityElement.text(response.total_quantity + ' шт.');
      },
      error: function(xhr, status, error) {
        // Обрабатываем ошибку при обновлении количества блюд
        console.error(error);
      }
    });
  }
});
