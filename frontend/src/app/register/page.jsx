'use client' // this signifies this component is on the "client" side of the app because it consumes an api https://react.dev/reference/react/use-client

import React, { useState } from 'react';
import { useRouter } from 'next/navigation'
import { GoogleLogin } from '@react-oauth/google'
import axios from 'axios';

import FastAPIClient from '../../client';
import config from '../../config';
import { Form, Button, Alert, InputGroup } from "react-bootstrap";

const client = new FastAPIClient(config);


const Register = () => {
  const [inputUsername, setInputUsername] = useState("");
  const [inputPassword, setInputPassword] = useState("");
  const [validated, setValidated] = useState(false);
  const [error, setError] = useState(false);
  const router = useRouter()

  // Standard user/password Registration
  const handleSubmit = (event) => {
    event.preventDefault();

    if(inputUsername.length <= 0){return setValidated(true);}
    if(inputPassword.length <= 0){return setValidated(true);}

    client.register(inputUsername, inputPassword)
      .then(() => {router.push("/")})
      .catch( (err) => {
        if (axios.isAxiosError(err)) {
          setError(err.message);
        } else {console.error(err);}
      });
  };

  function google_registration(response){
    client.register_google(response.credential)
    .then(() => {router.push("/")})
    .catch( (err) => {
      if (axios.isAxiosError(err)) {
        setError(err.message);
      } else {console.error(err);}
    });
  }

  return (
    <div>
      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        {error ? (
          <Alert variant="danger" onClose={() => setError(false)} dismissible>
            {error}
          </Alert>
        ) : (
          <div />
        )}
        <Form.Group>
          <Form.Label>Username</Form.Label>
          <InputGroup hasValidation>
            <Form.Control
              required
              type="text"
              value={inputUsername}
              placeholder="Username"
              onChange={(e) => setInputUsername(e.target.value)}
            />
            <Form.Control.Feedback type="invalid">Please enter a username.</Form.Control.Feedback>
          </InputGroup>
        </Form.Group>
        <Form.Group>
          <Form.Label>Password</Form.Label>
          <InputGroup hasValidation>
            <Form.Control
              required
              type="password"
              value={inputPassword}
              placeholder="Password"
              onChange={(e) => setInputPassword(e.target.value)}
            />
            <Form.Control.Feedback type="invalid">Please enter a password.</Form.Control.Feedback>
          </InputGroup>
        </Form.Group>
        <Button type="submit">Register</Button>
      </Form>

      <GoogleLogin
        onSuccess={credentialResponse => {
          console.log(credentialResponse);
          console.log(credentialResponse.credential);
          google_registration(credentialResponse);
        }}
        onError={() => {
          console.log('Login Failed');
        }}
      />;

    </div>
  );
};

export default Register;
