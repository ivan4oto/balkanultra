

function checkoutRedirect(preparedData) {
    // Get Checkout Session ID
    fetch(`/create_checkout_session/ultra`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(preparedData)
    })
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return Stripe(publicKey).redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  }


  
export { checkoutRedirect };