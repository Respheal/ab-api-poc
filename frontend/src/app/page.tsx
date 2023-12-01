'use client' // this signifies this component is on the "client" side of the app because it consumes an api https://react.dev/reference/react/use-client

import React, { useState, useEffect } from 'react';
import Link from 'next/link'
import axios from 'axios';

import FastAPIClient from '../client';
import config from '../config';

const client = new FastAPIClient(config);

export default function Home() {
  return (
  <main>
    <div>
      <p>hewwo O:</p>
      <Link href="/register">Dashboard</Link>
      <ApiExample />
    </div>
  </main>
  )
}

function ApiExample() {
  const [post, setPost] = useState<any>(null);

  useEffect(() => { //this causes the component to re-render if `post` is updated e.g. deleted https://react.dev/reference/react/useEffect
    async function getPost() {
      try {
        const response = await client.getComics(); // get response from client
        setPost(response.data); // update posts with response data
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.log("weh: " + error.message);
          console.log(error.response?.status); //optional chaining https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining
          console.log(error.response?.headers);
          console.log(error.response?.data);
        } else {
          console.error(error);
        }
      }
      const response = await client.getComic(1) // good request to preserve example
      setPost(response.data)
    }
    getPost();
  }, []); // you can add an attribute into this array to cause useEffect to *only* run if that attribute changes https://maxrozen.com/learn-useeffect-dependency-array-react-hooks

  async function deletePost() {
    await client.deleteComic(1);
    alert("Post deleted!");
    setPost(null);
  }

  if (!post) return "No post!"

  return (
    <div>
      <h1>{post.name}</h1>
      <p>{post.body}</p>
      <button onClick={deletePost}>Delete Post</button>
    </div>
  );
}



