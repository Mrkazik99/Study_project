import { Button, Container, Grid } from "@mui/material";

const Home = () => {
  return (
    <Container>
      <Grid container columns={2}>
        <Grid item>
          <a href="/customer">
            <Button>Jestem klientem</Button>
          </a>
        </Grid>
        <Grid item>
          <a href="/worker">
            <Button>Przejdź do panelu administracyjnego</Button>
          </a>
        </Grid>
      </Grid>
    </Container>
  );
};
export default Home;
