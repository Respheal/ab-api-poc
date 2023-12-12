'use client' // this signifies this component is on the "client" side of the app because it consumes an api https://react.dev/reference/react/use-client

import React, { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';

import { Comic } from '@/client';

export default function ComicPage({ params }: { params: { id: number } }) {
  const [post, setPost] = useState<any>(null);
  const { data } = useSession();

  useEffect(() => { //this causes the component to re-render if `post` is updated e.g. deleted https://react.dev/reference/react/useEffect
    async function getComic() {
      const comic = await Comic.getComic({id: params.id})
      if (comic) {setPost(comic.name)}
    }
    getComic();
  }, []); // you can add an attribute into this array to cause useEffect to *only* run if that attribute changes https://maxrozen.com/learn-useeffect-dependency-array-react-hooks

  // async function submitComic() {
  //   alert("Comic Created!");
  //   const comic = await Comic.createComic({name: "Comic Name Lorem"})
  //   if(comic){
  //     setPost(comic.name);
  //   }
  // }

  async function deletePost() {
    alert("Post deleted!");
    setPost(null);
  }

  if (data) { console.log(data) };


  return (
  <main>
    <div>
      <h1>{post}</h1>
      {data ? (
          <p>Access Token: {data.user.email}</p>
        ) : (
          <div />
        )}
      
      <button onClick={deletePost}>Delete Post</button>
      <form action="{Comic.createComic()}>"><button>Create Comic</button></form>
    </div>
  </main>
  )
}

