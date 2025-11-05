document.addEventListener('DOMContentLoaded',()=>{
   
    //찜 버튼
    const likeBtn = document.querySelector('.like');
    const likeCount = likeBtn.querySelector('.like-count');
    const heartSymbol = likeBtn.querySelector('.heart-symbol');
    let liked = false;

    likeBtn.addEventListener('click', () => {
        let count = parseInt(likeCount.textContent);

        if (!liked) {
            count += 1;
            likeCount.textContent = count;
            heartSymbol.textContent = '♥';

            likeBtn.classList.remove('animate-heart');
            void likeBtn.offsetWidth;
            likeBtn.classList.add('animate-heart');

            setTimeout(() => {
                likeBtn.classList.remove('animate-heart'); // 원래 크기로 돌아오기
            }, 200);
        } else {
            count -= 1;
            likeCount.textContent = count;
            heartSymbol.textContent = '♡';
        }
        
        liked = !liked;
    });

})