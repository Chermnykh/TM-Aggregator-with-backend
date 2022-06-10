console.log("Sanity check!");

console.log("Sanity check!");

// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

 
  // Event handler, Personal Plan
  let submitBtnPersonal = document.querySelector("#submitBtnPersonal");
  if (submitBtnPersonal !== null) {
    submitBtnPersonal.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session-personal/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }

  // Event handler, Family Plan
  let submitBtnFamily = document.querySelector("#submitBtnFamily");
  if (submitBtnFamily !== null) {
    submitBtnFamily.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session-family/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }

  // Event handler, Business Plan
  let submitBtnBusiness = document.querySelector("#submitBtnBusiness");
  if (submitBtnBusiness !== null) {
    submitBtnBusiness.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session-business/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }
});