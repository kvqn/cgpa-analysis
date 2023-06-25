import GradientLink from "@/components/GradientLink/GradientLink"
import { Navbar, NavbarItem } from "@/components/Navbar/Navbar"
import { getBatches } from "@/lib/data"

export const getStaticProps = async () => {
  const batches = await getBatches()
  return { props: { batches: batches } }
}

type Props = {
  batches: string[]
}

export default function Page({ batches }: Props) {
  return (
    <>
      <Navbar center={<NavbarItem name="Result" href="/result" active={true} />} />

      <div className="m-20">
        <h1 className="heading-select">Select your batch</h1>
        {batches.map((batch) => (
          <GradientLink href={`/result/${batch}`} name={batch} key={batch} />
        ))}
      </div>
    </>
  )
}