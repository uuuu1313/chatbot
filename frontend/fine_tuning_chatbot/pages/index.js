import React, { useState, useEffect } from 'react';

// config.js
export const BACKEND_URL = 'http://127.0.0.1:8000/';

const Home = () => {
    // 백엔드에서 가져온 데이터를 저장하는 상태(State)
    const [data, setData] = useState('');

    // useEffect 훅을 사용하여 컴포넌트가 마운트될 때 백엔드로부터 데이터를 가져오는 기능을 구현
    useEffect(() => {
        // '/api/hello' 엔드포인트를 사용하여 백엔드 API에서 데이터를 가져옴
        fetch(`${BACKEND_URL}api/hello`)
            .then((response) => response.json())
            .then((data) => setData(data));
    }, []);

    // 컴포넌트 JSX를 렌더링
    return (
        <div>
            <h1>Welcome to Fine_Tuning Chatbot !@#</h1>
            <p>{data}</p>
        </div>
    );
};

export default Home;