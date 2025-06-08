import os
import time 
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Experience, Education, Scraper, Interest, Accomplishment, Contact, Skill

class Person(Scraper):

    __TOP_CARD = "main"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(
        self,
        linkedin_url=None,
        name=None,
        about=None,
        experiences=None,
        educations=None,
        interests=None,
        accomplishments=None,
        skills=None, 
        company=None,
        job_title=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=True,
        time_to_wait_after_login=0,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.about = about or []
        self.experiences = experiences or []
        self.educations = educations or []
        self.interests = interests or []
        self.accomplishments = accomplishments or []
        self._skills = skills or []
        self.also_viewed_urls = []
        self.contacts = contacts or []

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") is None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), "drivers/chromedriver"
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")
                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)
        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    @property
    def skills(self):
        return self._skills

    @skills.setter
    def skills(self, value):
        self._skills = value

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_accomplishment(self, accomplishment):
        self.accomplishments.append(accomplishment)

    def add_skill(self, skill):
        self._skills.append(skill)

    def add_location(self, location):
        self.location = location

    def add_contact(self, contact):
        self.contacts.append(contact)

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print("You are not logged in!")

    def is_open_to_work(self):
        try:
            return "#OPEN_TO_WORK" in self.driver.find_element(By.CLASS_NAME,"pv-top-card-profile-picture").find_element(By.TAG_NAME,"img").get_attribute("title")
        except:
            return False

    def get_experiences(self):
            try:
                url = os.path.join(self.linkedin_url, "details/experience")
                self.driver.get(url)
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                self.scroll_to_half()
                self.scroll_to_bottom()
                main_list = self.wait_for_element_to_load(name="pvs-list__container", base=main)
                for position in main_list.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item"):
                    position = position.find_element(By.CSS_SELECTOR, "div[data-view-name='profile-component-entity']")
                    
                    # Fix: Handle case where more than 2 elements are returned
                    elements = position.find_elements(By.XPATH, "*")
                    if len(elements) < 2:
                        continue  # Skip if we don't have enough elements
                        
                    company_logo_elem = elements[0]
                    position_details = elements[1]

                    # company elem
                    try:
                        company_linkedin_url = company_logo_elem.find_element(By.XPATH,"*").get_attribute("href")
                        if not company_linkedin_url:
                            continue
                    except NoSuchElementException:
                        continue

                    # position details
                    position_details_list = position_details.find_elements(By.XPATH,"*")
                    position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
                    position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
                    
                    if not position_summary_details:
                        continue
                        
                    outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")

                    if len(outer_positions) == 4:
                        position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
                        company = outer_positions[1].find_element(By.TAG_NAME,"span").text
                        work_times = outer_positions[2].find_element(By.TAG_NAME,"span").text
                        location = outer_positions[3].find_element(By.TAG_NAME,"span").text
                    elif len(outer_positions) == 3:
                        if "·" in outer_positions[2].text:
                            position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
                            company = outer_positions[1].find_element(By.TAG_NAME,"span").text
                            work_times = outer_positions[2].find_element(By.TAG_NAME,"span").text
                            location = ""
                        else:
                            position_title = ""
                            company = outer_positions[0].find_element(By.TAG_NAME,"span").text
                            work_times = outer_positions[1].find_element(By.TAG_NAME,"span").text
                            location = outer_positions[2].find_element(By.TAG_NAME,"span").text
                    else:
                        position_title = ""
                        company = outer_positions[0].find_element(By.TAG_NAME,"span").text if outer_positions else ""
                        work_times = outer_positions[1].find_element(By.TAG_NAME,"span").text if len(outer_positions) > 1 else ""
                        location = ""

                    # Safely extract times and duration
                    if work_times:
                        parts = work_times.split("·")
                        times = parts[0].strip() if parts else ""
                        duration = parts[1].strip() if len(parts) > 1 else None
                    else:
                        times = ""
                        duration = None

                    from_date = " ".join(times.split(" ")[:2]) if times else ""
                    to_date = " ".join(times.split(" ")[3:]) if times and len(times.split(" ")) > 3 else ""
                    
                    if position_summary_text and any(element.get_attribute("class") == "pvs-list__container" for element in position_summary_text.find_elements(By.XPATH, "*")):
                        try:
                            inner_positions = (position_summary_text.find_element(By.CLASS_NAME,"pvs-list__container")
                                            .find_element(By.XPATH,"*").find_element(By.XPATH,"*").find_element(By.XPATH,"*")
                                            .find_elements(By.CLASS_NAME,"pvs-list__paged-list-item"))
                        except NoSuchElementException:
                            inner_positions = []
                    else:
                        inner_positions = []
                    
                    if len(inner_positions) > 1:
                        descriptions = inner_positions
                        for description in descriptions:
                            try:
                                res = description.find_element(By.TAG_NAME,"a").find_elements(By.XPATH,"*")
                                position_title_elem = res[0] if len(res) > 0 else None
                                work_times_elem = res[1] if len(res) > 1 else None
                                location_elem = res[2] if len(res) > 2 else None

                                location = location_elem.find_element(By.XPATH,"*").text if location_elem else None
                                position_title = position_title_elem.find_element(By.XPATH,"*").find_element(By.TAG_NAME,"*").text if position_title_elem else ""
                                work_times = work_times_elem.find_element(By.XPATH,"*").text if work_times_elem else ""
                                
                                # Safely extract times and duration
                                if work_times:
                                    parts = work_times.split("·")
                                    times = parts[0].strip() if parts else ""
                                    duration = parts[1].strip() if len(parts) > 1 else None
                                else:
                                    times = ""
                                    duration = None
                                    
                                from_date = " ".join(times.split(" ")[:2]) if times else ""
                                to_date = " ".join(times.split(" ")[3:]) if times and len(times.split(" ")) > 3 else ""

                                experience = Experience(
                                    position_title=position_title,
                                    from_date=from_date,
                                    to_date=to_date,
                                    duration=duration,
                                    location=location,
                                    description=description,
                                    institution_name=company,
                                    linkedin_url=company_linkedin_url
                                )
                                self.add_experience(experience)
                            except (NoSuchElementException, IndexError) as e:
                                # Skip this description if elements are missing
                                continue
                    else:
                        description = position_summary_text.text if position_summary_text else ""

                        experience = Experience(
                            position_title=position_title,
                            from_date=from_date,
                            to_date=to_date,
                            duration=duration,
                            location=location,
                            description=description,
                            institution_name=company,
                            linkedin_url=company_linkedin_url
                        )
                        self.add_experience(experience)
            except Exception as e:
                print(f"WARNING: Error getting experiences: {e}")
                self.experiences = []
                

    
    def get_educations(self):
        url = os.path.join(self.linkedin_url, "details/education")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list__container", base=main)
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-list__paged-list-item"):
            try:
                position = position.find_element(By.CSS_SELECTOR, "div[data-view-name='profile-component-entity']")
                
                # Fix: Handle case where more than 2 elements are returned
                elements = position.find_elements(By.XPATH,"*")
                if len(elements) < 2:
                    continue  # Skip if we don't have enough elements
                    
                institution_logo_elem = elements[0]
                position_details = elements[1]

                # institution elem
                try:
                    institution_linkedin_url = institution_logo_elem.find_element(By.XPATH,"*").get_attribute("href")
                except NoSuchElementException:
                    institution_linkedin_url = None

                # position details
                position_details_list = position_details.find_elements(By.XPATH,"*")
                position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
                position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
                
                if not position_summary_details:
                    continue
                    
                outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")

                institution_name = outer_positions[0].find_element(By.TAG_NAME,"span").text if outer_positions else ""
                degree = outer_positions[1].find_element(By.TAG_NAME,"span").text if len(outer_positions) > 1 else None

                from_date = None
                to_date = None
                
                if len(outer_positions) > 2:
                    try:
                        times = outer_positions[2].find_element(By.TAG_NAME,"span").text

                        if times and "-" in times:
                            split_times = times.split(" ")
                            dash_index = split_times.index("-") if "-" in split_times else -1
                            
                            if dash_index > 0:
                                from_date = split_times[dash_index-1]
                            if dash_index < len(split_times) - 1:
                                to_date = split_times[-1]
                    except (NoSuchElementException, ValueError):
                        from_date = None
                        to_date = None

                description = position_summary_text.text if position_summary_text else ""

                education = Education(
                    from_date=from_date,
                    to_date=to_date,
                    description=description,
                    degree=degree,
                    institution_name=institution_name,
                    linkedin_url=institution_linkedin_url
                )
                self.add_education(education)
            except (NoSuchElementException, IndexError) as e:
                # Skip this education entry if elements are missing
                continue


    def get_name_and_location(self):
        try:
            top_panel = self.driver.find_element(By.XPATH, "//*[@class='mt2 relative']")
            self.name = top_panel.find_element(By.TAG_NAME, "h1").text
            self.location = top_panel.find_element(By.XPATH, "//*[@class='text-body-small inline t-black--light break-words']").text
        except Exception as e:
            print(f"WARNING: Error getting name/location: {e}")

    def get_about(self):
        try:
            about = self.driver.find_element(By.ID,"about").find_element(By.XPATH,"..").find_element(By.CLASS_NAME,"display-flex").text
        except NoSuchElementException:
            about = None
        self.about = about

    def get_skills(self):
        print("DEBUG: Scraping skills.")
        try:
            self.scroll_to_bottom()
            sleep(1)
            skills_section = self.driver.find_element(By.ID, "skills")
            skill_elements = skills_section.find_elements(By.XPATH, ".//span[contains(@class, 'pv-skill-category-entity__name-text')]")
            self._skills = [Skill(name=elem.text.strip()) for elem in skill_elements if elem.text.strip()]
            print(f"DEBUG: Found {len(self._skills)} skills.")
        except Exception as e:
            print(f"WARNING: Error getting skills: {e}")
            self._skills = []

    def get_interests(self):
        print("DEBUG: Attempting to scrape interests.")
        try:
            self.driver.get(self.linkedin_url + "details/interests/")
            sleep(2)
            interest_elements = self.driver.find_elements(By.XPATH, "//span[contains(@class,'entity-result__title-text')]")
            self.interests = [Interest(title=elem.text.strip()) for elem in interest_elements if elem.text.strip()]
            print(f"DEBUG: Found {len(self.interests)} interests.")
        except Exception as e:
            print(f"WARNING: Error getting interests: {e}")
            self.interests = []

    def get_accomplishments(self):
        print("DEBUG: Attempting to scrape accomplishments.")
        try:
            self.driver.get(self.linkedin_url + "details/accomplishments/")
            sleep(2)
            accomplishment_sections = self.driver.find_elements(By.XPATH, "//section[contains(@class, 'artdeco-card')]")
            for section in accomplishment_sections:
                try:
                    category_elem = section.find_element(By.TAG_NAME, "h2")
                    category = category_elem.text.strip()
                    items = section.find_elements(By.XPATH, ".//li")
                    for item in items:
                        title = item.text.strip()
                        if title:
                            self.accomplishments.append(Accomplishment(category=category, title=title))
                except Exception:
                    continue
            print(f"DEBUG: Found {len(self.accomplishments)} accomplishments.")
        except Exception as e:
            print(f"WARNING: Error getting accomplishments: {e}")
            self.accomplishments = []

   
    def get_contacts(self):
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        contacts = {}

        # Close any open overlays/modals that might block the click
        try:
            close_btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
            close_btn.click()
            time.sleep(1)
        except:
            pass

        # Click the Contact Info button
        try:
            contact_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "top-card-text-details-contact-info"))
            )
            contact_btn.click()
        except Exception as e:
            print(f"Could not click Contact Info button: {e}")
            self.contacts = contacts
            return

        # Wait for the overlay and loader to disappear
        try:
            overlay = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "artdeco-modal__content"))
            )
            WebDriverWait(self.driver, 10).until_not(
                EC.visibility_of_element_located((By.CLASS_NAME, "artdeco-loader"))
            )
            time.sleep(0.5)
            # Re-acquire the overlay element after loader disappears to avoid stale element reference
            overlay = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "artdeco-modal__content"))
            )
        except Exception as e:
            print(f"Contact Info overlay did not appear: {e}")
            self.contacts = contacts
            return

        # Extract Email
        try:
            email_elem = overlay.find_element(By.XPATH, ".//a[starts-with(@href, 'mailto:')]")
            contacts['email'] = email_elem.text.strip()
        except:
            contacts['email'] = None

        # Extract Phone
        try:
            phone_elem = overlay.find_element(By.XPATH, ".//a[starts-with(@href, 'tel:')]")
            contacts['phone'] = phone_elem.text.strip()
        except:
            contacts['phone'] = None

        # Extract Websites
        try:
            website_elems = overlay.find_elements(By.XPATH, ".//a[starts-with(@href, 'http')]")
            contacts['websites'] = [w.get_attribute("href") for w in website_elems if w.get_attribute("href")]
        except:
            contacts['websites'] = []

        # Close the overlay
        try:
            close_btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
            close_btn.click()
        except:
            pass

        self.contacts = contacts



    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, self.__TOP_CARD))
        )
        self.focus()
        self.wait(5)
        self.get_name_and_location()
        self.open_to_work = self.is_open_to_work()
        self.get_about()
        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")
        sleep(1)
        self.get_experiences()
        self.get_educations()
        self.get_skills()
        self.get_interests()
        self.get_accomplishments()
        self.get_contacts()
        if close_on_complete:
            driver.quit()
