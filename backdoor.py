from app import DebugableApp
import WebsiteAPI

def main():
    debugable_app = DebugableApp()

    WebsiteAPI.create_post(
        'meng981306@gmail.com', 
        'Software Developer & Others- New Grad - Sunnyvale 0023',
        '''Job Description 
Sunnyvale CA United States

Are you the next FORTIHIRE?

Fortinet Teams are looking for NEW GRADS (2017-2018) for a variety of skill domains such as Software Developers, Embedded Software Engineers, Web Developers, Software Dev QA Engineers, Release QA Engineers, ASIC Engineers, Hardware Development Engineers and more.

With the ever growing global demand to secure networks in the face of emerging new threats and data breaches, there is a greater need to provide end-to-end, next generation Security products for integrated and customized solutions to secure enterprises on different scales. The Network/Cyber Security Industry is poised to grow from 75 Billion (current) to 175 Billion Dollar industry by 2020. So if you are up for a challenge and a career in our Industry, Fortinet is at the forefront and offers you the opportunity to get a dream start to your career!

Our 2016 global headcount growth was 35%. This growth is continuing in 2017 and our R&D teams inSunnyvale offer great opportunities for new grads. We value the talent new grads add to our teams every year and we respect academic excellence as well as innovative minds.
The Sunnyvale R&D location is our Head Office and one of our core technology hub with experts in the Engineering field. Our salaries are competitive and we also offer Stock grants/Stock options in addition to a great benefits package.

We would like to invite NEW GRADs of 2017 to register by applying to this posting and uploading your resume so that our team is able to review your profile. Please note that this posting is specifically meant for new graduates only who have recently graduated and those who are about to graduate and available for full time opportunities between now and Spring 2018. Whether you are interested in a Software developer role or QA or C Programmer or Web Developer or Hardware Engineer or ASIC Engineering, we encourage you to apply here and our recruitment team will contact you further for initial screening. For experienced candidates, there are postings available on our careers page where they can register and apply for other openings.

Please don't forget to mention your availability (for full time role), career interest (Software/Embedded/Hardware/Hardware/ASIC/QA and others) and work eligibility either as a part of your application or on top of your resume. We will carefully review your application and contact you by following up with a call or email.
Thank you for your response and we are looking forward to talking to you''', 
        2, debugable_app.website)

    WebsiteAPI.create_post(
        'gmatti1@asu.edu', 
        'Software Engineer Internship (Northbrook, IL)',
        '''The Opportunity
Consumer connectivity is growing every day-across our cars, smartphones, homes, and in virtually every aspect of our lives. We recognized this trend when we launched Drivewise in 2010, and we haven't stopped accelerating since. When you join our technology team, you’ll have the freedom to dream up amazing innovations and explore new technologies. We're looking for technology visionaries who aren't afraid to rethink the way things work.
Today, our telematics sensors now connect more than 1,000,000 consumers, and our mobile user experiences are helping to make our customer's driving experiences more informative, engaging, and fun. So we're not overpromising when we say that at Allstate, you can make an impact on the future of the driving experience and in how consumers connect across the Internet of Things.''',
        1, debugable_app.website)

    WebsiteAPI.create_post(
        'aneeshdalvi143@gmail.com', 
        'Software QA Engineering Internship (Spring 2019)',
        '''Columbia College Chicago students: Columbia College Chicago does not have Co-op Education program. You must accept this opportunity as an internship. For academic credit, please contact your Internship and Career Advisor.''',
        1, debugable_app.website)

    WebsiteAPI.create_post(
        'jkdrumm@asu.edu', 
        'JR0071614 Undergraduate Intern 2019 - Industrial Engineering',
        '''This is a Summer 2019 Intern Position. The candidate will join CPLG (Customer Fulfillment, Planning and Logistics Group) and will be working on process & capability development, reporting & customer fulfillment management.''',
        1, debugable_app.website)

    WebsiteAPI.create_post(
        'virajtalaty@gmail.com', 
        'Software Engineer - New Grad - San Francisco',
        '''Dropbox is a leading global collaboration platform that's transforming the way people work together, from the smallest business to the largest enterprise. With more than 500 million registered users across more than 180 countries, our mission is to unleash the world's creative energy by designing a more enlightened way of working.''',
        1, debugable_app.website)


    debugable_app.website.app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    main()
