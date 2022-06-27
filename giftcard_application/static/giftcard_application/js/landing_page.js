var coin_flip_heads = document.getElementById('wrapper_flip_coin_result_img_heads');
      var coin_flip_tails = document.getElementById('wrapper_flip_coin_result_img_tails');
      var giftcard_img = document.getElementById('giftcard_img');

      var giftcard_message = document.getElementById('giftcard_message_wrapper');

      var generate_giftcard_btn = document.getElementById('generate_giftcard_btn');
      var flip_coin_btn = document.getElementById('flip_coin_button');

      var score_system_heads = document.getElementById('heads_count');
      var score_system_tails = document.getElementById('tails_count');

      var heads_count = 0;
      var tails_count = 0;

      score_system_heads.innerHTML = heads_count;
      score_system_tails.innerHTML = tails_count;

      //scoreboard
      scoreboard_list = document.getElementById('scoreboard_wrapper_container_list')

      flip_coin_btn.disabled = true;

      async function makeCard(){

        //Hide both heads and tails.
        coin_flip_heads.style.display = 'none';
        coin_flip_tails.style.display = 'none';

        //When new card is created then user can add stuff again
        flip_coin_btn.disabled = false;


        //Reset the counter globally when a new giftcard is made
        //Reset the content of div
        reset_counter();
        disable_generate_giftcard();


      console.log('function activated');
      var giftcard_url = "{% url 'giftcard_api:giftcards' %}";



       await fetch(giftcard_url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
            },

        })
      .then((resp) => {

      if (resp.status === 200){
        console.log(resp)
        return resp.json()
        }
      throw new Error("The dates could not be fetched.")
      })
      .then(function(data){
          console.log(data);
          //Sets global variable

          card_number = data.identifier;
          gift_card_info = data;
          giftcard_created_message();
          disable_button();
      })
      .catch((error) => {
      console.log(error)
      });

    }

    function disable_generate_giftcard(){
        generate_giftcard_btn.disabled = true;
        giftcard_img.style.display = 'none';
        return
      }


    function reset_counter(){
      heads_count = 0;
      tails_count = 0;

      score_system_heads.innerHTML = 0;
      score_system_tails.innerHTML = 0;
    }

    function giftcard_created_message(){

        const message = `giftcard has been issued ! `

        //Pass this message to a toast or something

        return
    }

    async function payForCoinFlip(){

      giftcard_message.innerHTML = ``

      var coin_flip_wrapper = document.getElementById('flip_coin');
      if (typeof card_number !== 'undefined') {
        
         var giftcard_detail_url = "{% url 'giftcard_api:giftcards' %}" + card_number + "/details/";
          
          

        await fetch(giftcard_detail_url, {
                method: 'PATCH',
                headers: {
                  'Content-Type': 'application/json',
              },
          })
        .then((resp) => {

        if (resp.status === 200){

          console.log(resp)
          return resp.json()

          }
        throw new Error("The dates could not be fetched.")
        })
        .then(function(data){

          console.log(data);

          coinFlip(); 

          const credit_rem = data.credit_remaining;

          if (credit_rem == 0){
            console.log("If credit_remaining = 0 then disable button");
            disable_flip_button();
            calculate_head_tail_ratio_stat();
            submit_to_scoreboard();
            allow_generate_giftcard();

          } 

          return


        })
        .catch((error) => {
        console.log(error)
        });
      } else {


        console.log("type not defined");
        alert("code from here on out doesn't work");
        const message = `<p class="error_coin_flip>Please Generate A Gift Card First..</p>`;

        coin_flip_wrapper.innerHTML = message;
        }

      }



      function disable_flip_button(){
        flip_coin_btn.disabled = true;
        return
      }



      function coinFlip(){
        console.log("Thanks for playing !");

        var heads_tails = Math.round(Math.random());

        if (heads_tails == 1){

          coin_flip_heads.style.display = 'block';
          coin_flip_tails.style.display = 'none';

          score_system_heads.innerHTML = ++heads_count;
          

          return

        } else {

          coin_flip_heads.style.display = 'none';
          coin_flip_tails.style.display = 'block';
          
          score_system_tails.innerHTML = ++tails_count;
    
          

          return

        }

      }



      function calculate_head_tail_ratio_stat(){
        heads_statistic = heads_count / 25;
        tails_statistic = tails_count / 25;

        alert("probability of heads: " + heads_statistic + "\n  probability of tails: " + tails_statistic);

        return

      }


      function allow_generate_giftcard(){
        generate_giftcard_btn.disabled = false;
        giftcard_img.style.display = 'none';
        return
      }

      async function submit_to_scoreboard(){
        var scoreboard_url = "{% url 'giftcard_api:scoreboard' %}";

        data = {
          'probability_heads': heads_statistic,
          'probability_tails': tails_statistic,
        }


        await fetch(scoreboard_url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
          })
        .then((resp) => {

        if (resp.status === 200){
          console.log(resp)
          return resp.json()
          }
        throw new Error("The dates could not be fetched.")
        })
        .then(function(data){
            
            //We want to append the data after the game ends.
            
            var row = `
              <div class="row">
                <div class="col">
                  ${data.score_id}
                </div>
                <div class="col">
                  ${data.probability_heads}
                </div>
                <div class="col">
                  ${data.probability_tails}
                </div>
              </div>

            `

            scoreboard_list.innerHTML += row;

        })
        .catch((error) => {
        console.log(error)
        });

      }

      //begin this function upon page load

      get_scoreboard();

      async function get_scoreboard(){
        var scoreboard_url = "{% url 'giftcard_api:scoreboard' %}";

        await fetch(scoreboard_url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          })
        .then((resp) => {

        if (resp.status === 200){
          console.log(resp)
          return resp.json()
          }
        throw new Error("The dates could not be fetched.")
        })
        .then(function(data){
          console.log(data);
          build_scoreboard(data);
          create_heads_tails_array(data);
          addData_graphs();

        })
        .catch((error) => {
        console.log(error)
        });

      }

      function build_scoreboard(data){
        if (data.length == 0){
          message = "Sorry but there are no scores yet.";
          return message;
        } else {

          for (var i in data){

            data_entry = data[i];

            var row = `
              <div class="row">
                <div class="col">
                  ${data_entry.score_id}
                </div>
                <div class="col">
                  ${data_entry.probability_heads}
                </div>
                <div class="col">
                  ${data_entry.probability_tails}
                </div>
              </div>

            `

            scoreboard_list.innerHTML += row;

          }
          return
      
          //for every item in the data, place it in score board container.

        }
      }


      function create_heads_tails_array(data){
        
        //Data needs to be in particular format
        //To be consumed by graphs.

        list_all_heads = [];
        list_all_ids = []
        list_all_tails = [];

        for (var i in data){

            data_entry = data[i];
            list_all_heads.push(data_entry.probability_heads);
            list_all_tails.push(data_entry.probability_tails);
            list_all_ids.push(data_entry.score_id);
      }
      return
    }

    function addData_graphs(){
      headChart.data.labels.push(list_all_ids);
      headChart.data.datasets.forEach((dataset) => {
          dataset.data.push(list_all_heads);
      });
      headChart.update();

      tailChart.data.labels.push(list_all_ids);
      tailChart.data.datasets.forEach((dataset) => {
          dataset.data.push(list_all_tails);
      });
      tailChart.update();

    }
   

      //fetch all score data,
      //find average of all heads and feed into graphy
      //Do same with tails

      const head = document.getElementById('heads_chart').getContext('2d');
      const headChart = new Chart(head, {
          type: 'line',
          data: {
              labels: [],
              datasets: [{
                  data: [],
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                  
                      
                  ],
                  borderColor: [
                      'rgba(255, 99, 132, 1)',
         
                     
                  ],
                  borderWidth: 0.2
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });


      const tail = document.getElementById('tails_chart').getContext('2d');
      const tailChart = new Chart(tail, {
          type: 'line',
          data: {
              labels: [],
              datasets: [{
                  data: [],
                  backgroundColor: [
                   
                      'rgba(54, 162, 235, 0.2)',
                      
                  ],
                  borderColor: [
      
                      'rgba(54, 162, 235, 1)',
                     
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });