import streamlit as st

from utils import post_feedback, resize_image, save_rate,get_recommended_beer,get_info,get_grid,get_cols,post_feedback, get_init_beers
from config import CGF

#################################
# 맥주 DB
# TODO DB를 연동해 주세요

beer_dict = {'Sapporo Premium Beer / Draft Beer':'729', 'Tsingtao Premium Stout 4.8%':'567803',
'Tsingtao Draft Beer 11º (Pure Draft Beer)':'64518', 'Heineken':'37',
'Heineken Dark Lager':'34662', 'Heineken Premium Light':'48076'}

beer_list = ['Sapporo Premium Beer / Draft Beer', 'Tsingtao Premium Stout 4.8%', 'Tsingtao Draft Beer 11º (Pure Draft Beer)',
'Heineken', 'Heineken Dark Lager', 'Heineken Premium Light', 'Heineken Premium Light', 'Heineken Premium Light', 'Heineken Premium Light', 
'Heineken Premium Light', 'Heineken Premium Light', 'Heineken Premium Light']

beer_img_link = ['https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_729',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_567803',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_64518',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_37',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_34662',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_48076',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_48076',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_48076',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_48076',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_48076',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_48076',
'https://res.cloudinary.com/ratebeer/image/upload/d_beer_img_default.png,f_auto/beer_48076',]


#################################
# 저장변수
coldstart_data = {}
keywords=[]

##################################
# streamlit 실행.
st.title("도전맥주홀릭")

# coldstart 맥주 평가
st.header("맥주에 대해 평가해 주세요")

# streamlit은 grid 방식을 지원하지 않기 때문에 columns로 hard coding 
row, col = get_grid(CGF.num_items)
total_cols = get_cols(row, col)
beer_list ,beer_img_link =get_init_beers(beer_list, beer_dict)

for col, beer, image_path in zip(total_cols, beer_list , beer_img_link): 
    # TODO beer_list,beer_img_link 는 DP와 연동해주세요
    with col:
        st.image(resize_image(image_path, CGF.image_size))
        option_rate = st.radio(
            beer, CGF.options, key = col
        )
        save_rate(beer_dict, beer, option_rate, coldstart_data)


# 추천 키워드 선택
st.header("추천에 원하는 키워드를 선택해보세요")
keywords = st.multiselect('여러개 선택가능!', CGF.rec_keywords)

# coldstart 맥주 평가 제출
coldstart_button = st.button('제출')

if coldstart_button: 
    st.write(coldstart_data)
    st.write(keywords)
    # TODO 여기서 POST를 해주세요
    

    # 4캔 추천 반환
    st.header("추천결과!")
    r_beer_id = get_recommended_beer()
    r_beers = {beer_id:get_info(beer_id) for beer_id in r_beer_id}

    r_col1, r_col2, r_col3, r_col4 = st.columns(4)
    r_cols = [r_col1, r_col2, r_col3, r_col4]
    for col, beer_id in zip(r_cols, r_beer_id):
        with col:
            st.image(resize_image(r_beers[beer_id]['imageUrl'], CGF.image_size),
                    caption = r_beers[beer_id]['beerName'])


    # 추천 결과 평가(TODO 수정해야함 - if문 안에서 버튼은 다음 액션으로 이어지지 않음)
    st.header("추천 결과는 어떤가요? 피드백ㄱㄱ")

    submit_result = st.button("좋아요")        
    submit_result = st.button("싫어요")  
    if submit_result:
        st.write("해써")
        st.write(post_feedback(r_beer_id, submit_result))

