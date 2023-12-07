'use client'

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Link from 'next/link'
import { usePathname } from 'next/navigation';

function Navigation() {

  const pathname = usePathname();

  return (
    <Navbar expand="lg" className="bg-body-tertiary" collapseOnSelect>
      <Container>
        <Navbar.Brand href="/">AB POC</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav variant="tabs" className="me-auto" defaultActiveKey="/">
            <Nav.Link as={Link} active={pathname == "/" ? true : false } eventKey="1" href="/">Some Page</Nav.Link>
            <Nav.Link as={Link} active={pathname == "/register" ? true : false } eventKey="2" href="/register">Some Page</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navigation;