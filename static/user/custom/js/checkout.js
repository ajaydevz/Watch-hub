$(document).ready(function () {

    
    $('.paywithRazorpay').click(function (e) {
        e.preventDefault();
        console.log("Clicked the payWithRazorpay button");
        var address_id = $("[name='selected_address']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();


        if (address_id == "" ) {
            Swal.fire(
                'Alert!',
                'Please select any of address or kindly create a new one !',
                'error'
            )
            return false;
        } else {
            $.ajax({
                url: '/cart/proceed-to-pay/', // The URL you want to request
                method: 'GET', // HTTP request method (GET, POST, PUT, DELETE, etc.)
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                    // Callback function to handle the successful response
                    var options = {
                        "key": "rzp_test_Rfp1v8lrP3e3e1",
                        "amount": data.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name":  'ASWIN',
                        "description": "Thank you",
                        "image": "https://example.com/your_logo",
                        //                    "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the id obtained in the response of Step 1
                        "callback_url": "https://eneqd3r9zrjok.x.pipedream.net/",
                        "handler": function (response) {
                            data = {
                                'selected_address': address_id,
                                'payment_mode': 'Paid by Razorpay',
                                'payment_id': response.razorpay_payment_id,
                                csrfmiddlewaretoken: token,

                            };
                            $.ajax({
                                url: '/cart/place-order/',
                                method: 'POST',
                                data: data,
                                
                                success: function (responseData) {
                                console.log(responseData);
                                    swal({
                                        title: "Congratulations!",
                                        text: "Your order has been placed successfully",
                                        icon: "success",
                                        buttons: true,
                                        dangerMode: true,
                                    }).then((willDelete) => {
                                        if (willDelete) {
                                        console.log('...........');
                                            window.location.href = '/cart/order-success'
                                        } else {
                                            swal("Your imaginary file is safe!");
                                        }
                                    });

                                },
                                error: function (error) {
                                    // Callback function to handle errors
                                    console.error('Error:', error);
                                }
                            });
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information especially their phone number
                            "name": "username", //your customer's name
                            "email": "email",
                            "contact": 9400127849, //Provide the customer's phone number for better conversion rates
                        },

                        //                    "notes": {
                        //                        "address": "Razorpay Corporate Office"
                        //                    },
                        "theme": {
                            "color": "#3399cc"
                        },
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                },
                // error: function (error) {
                //     // Callback function to handle errors
                //     console.error('Error:', error);
                
            });
        }
    });







});