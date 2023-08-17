import React, {useState, useEffect} from 'react'
import './Posts.css'

import Accordion from 'react-bootstrap/Accordion';

function Post({setPosts, posts}) {

    

    useEffect(() => {
      fetch("/fjdksafhkdsafldnsajk/posts").then(
        res => res.json()
        
      ).then(
        data => {
          setPosts(data)
        }
      )
    },[]);


  return (
    <div className="Post-Div">
      {Object.entries(posts).map(post=>{
       return(
        <Accordion defaultActiveKey="1" flush>
      <Accordion.Item eventKey="0">
        <Accordion.Header>
            <div className="post-title" >
                <div><p>{post[0]}</p></div>
                <div><p>{post[1].Time}</p></div>
            </div>
        </Accordion.Header>
        <Accordion.Body>
        <div>
        <h4>Headers</h4>
          {Object.entries(post[1].Headers).map(([key,value]) =>{
            return(<p>{key} : {value}</p>)
          })}
        </div>
        <div>
        <h4>Body</h4>
          {Object.entries(post[1].Body).map(([key,value]) =>{
            return(<p>{key} : {value}</p>)
          })}
        </div>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
       )
      })}
    </div>
  );
}

export default Post;