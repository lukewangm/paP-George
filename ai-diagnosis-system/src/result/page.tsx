import { useRouter } from 'next/router';

const result = () => {
  const router = useRouter();
  const { data } = router.query; // Access the query parameter

  const parsedData = data ? JSON.parse(data) : null; // Parse the data

  return (
    <div>
      <h1>Received Data</h1>
      <pre>{JSON.stringify(parsedData, null, 2)}</pre>
    </div>
  );
};

export default result;