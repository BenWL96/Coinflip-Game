# Coinflip-Game
##Redeem your giftcard, flip a coin, and see your score under games played. 

This project acts as a proof of concept for basic utilisation of the Django Rest Framework.
The API uses:

- POST AND GET function based API views in order to create the giftcards
- UPDATE in order to reduce the credit value which is remaining on the giftcard
- POST AND GET to post final score to endpoint.

When a new player arrives, they are promted to create a card which has £25 on. Whenever they press 'flip-coin'
£1 is removed from the card, until all their credit has been used.

The project uses HTML, Bootstrap and Javascript, in order create a responsive user experience.
