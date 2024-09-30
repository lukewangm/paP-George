export default function About() {
    return <div >
        <p className="flex justify-center border-2 border-black"> Each page directory requires a page.tsx file </p>

        <br></br>

        <p className="flex justify-center">
            I will be using tailwind css for this project, you can learn more:
            <a className="bg-[#fecaca]" href="https://tailwindcss.com/docs/installation">here</a>
        </p>

        <br></br>

        <h3 className="flex justify-center text-4xl ">Frontend Architecture</h3>
        <ul className="list-disc pl-10">
            <li> React with Next.JS framework</li>
            <li> Tailwind css</li>
        </ul>

        </div>
  }