import React, {useState, useEffect} from 'react'
import Footer from './Components/Footer/Footer'
import Post from './Components/Posts/Post'
import Header from './Components/Header/Header'
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [posts, setPosts] = useState({})

const LoadData = () =>{
  fetch("/fjdksafhkdsafldnsajk/posts").then(
    res => res.json()
    
  ).then(
    data => {
      setPosts(data)
      console.log(data)
    }
  )
}

  return (
    <div className="App">
      <Header />
       {Object.keys(posts).length === 0 ? <button onClick={()=>{LoadData()}}>Load</button> : <Post posts={posts} setPosts={setPosts}/> }
      <Footer />
    </div>
  );
}

export default App;
