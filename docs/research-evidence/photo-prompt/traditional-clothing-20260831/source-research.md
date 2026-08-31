# Traditional clothing visual-semantics research

Reviewed: 2026-08-31

## Scope and decision boundary

This research converts named garments and textile techniques into observable photographic evidence. It does not infer a wearer's ethnicity, nationality, religion, clan, caste, region, social status, gender identity, or authenticity from clothing. A garment label is never satisfied by face shape, hair, skin tone, architecture, landscape, palette, a national flag, or an ornamental prop.

The runtime model separates four layers:

1. garment topology: upper and lower pieces, panel count and direction, opening, overlap, collar, sleeve, waist, hem, and body coverage;
2. wearing mechanism: fastening, tying, tucking, wrapping, pleating, belting, and layer order;
3. qualified context: region, period, documented form, occasion, climate, and wearer-specific styling;
4. textile construction: woven, embroidered, resist-dyed, yarn-dyed, supplementary-weft, printed, or applied decoration.

Exact stable garment terms can activate a narrow visual contract only when their garment context is present. Descriptive paraphrases, BM25F hits, embedding hits, colors, motifs, locations, and nearby garments remain advisory until selected. The broad labels `traditional dress`, `folk costume`, `ethnic costume`, `tribal dress`, `Asian robe`, `전통 의복`, `민속 의상`, and `민족 의상` never select a named garment profile.

## Garment matrix

| Garment family | Observable construction owned by the candidate | Important confusion boundary | Source |
| --- | --- | --- | --- |
| Hanbok | short jeogori upper layer; tied front; separate chima or baji; readable layer boundary | palace, pastel color, hairstyle, or wide sleeves alone | National Folk Museum of Korea: https://www.nfm.go.kr/k-box/ui/hanbok/female.do?lang=en and https://www.nfm.go.kr/k-box/ui/hanbok/male.do?lang=en |
| Kimono | straight sewn panels; wrapped front; sleeve depth; separate obi layer | generic robe, blossom prop, or obi-like belt alone | V&A: https://www.vam.ac.uk/articles/kimono |
| Hanfu | period-qualified collar direction, upper/lower layers, sleeve and sash relationship | cross-collar plus wide sleeves is shared across several East Asian systems and cannot select a dynasty | China National Silk Museum: https://www.chinasilkmuseum.com/gwgk/info_4.aspx?itemid=26485&lcid=628 |
| Qipao / cheongsam | standing collar connected to curved or diagonal opening; frog fastenings; continuous body; coherent side construction | Mandarin collar, bodycon fit, or side slit alone | Hong Kong Museum of History: https://hk.history.museum/en/web/mh/exhibition/2010_past_04.html and PolyU: https://www.polyu.edu.hk/sft/-/media/department/sft/publication/shows-and-exhibitions/youth--beauty-brochure.pdf |
| Sari | one continuous cloth wrapped around the body with a traceable free end; supporting blouse and underskirt may be present | stitched gown plus detached scarf | V&A: https://www.vam.ac.uk/articles/indian-textiles |
| Nivi sari | continuous cloth; waist wrap; aligned front pleats; torso crossing; left-shoulder pallu | this route must not be generalized to every regional sari drape | V&A: https://www.vam.ac.uk/articles/indian-textiles and clothing-climate study: https://escholarship.org/uc/item/0080t60q |
| Ao dai | long close-cut front/back tunic panels; long side openings; separate trousers | one long dress without separate trousers | Vietnam Tourism: https://vietnam.travel/node/1216 |
| Kebaya | shaped front-opening upper garment; fine embroidered/lace/light cloth; functional center fastening; separate wrapped lower layer | generic lace blouse, brooch, or sarong alone | UNESCO ICH: https://ich.unesco.org/en/RL/kebaya-knowledge-skills-traditions-and-practices-02090 |
| Barong Tagalog | formal shirt worn untucked; fine lightly translucent cloth; readable placket and concentrated embroidery; opaque underlayer | generic sheer shirt or embroidered resort top | Cultural Center of the Philippines: https://culturalcenter.gov.ph/press-release/how-the-baro-transformed-into-the-garment-of-filipino-identity/ |
| Moroccan caftan | long robe body; continuous center-front trim/fastening; hand decoration; optional broad mdamma belt | jeweled gown or generic belted robe | UNESCO ICH: https://ich.unesco.org/en/RL/moroccan-caftan-art-traditions-and-skills-02077?RL=02077 |
| Huipil | rectangular woven panels joined around a deliberate neck opening; panel-scale weave or embroidery zones | printed bohemian tunic | V&A: https://www.vam.ac.uk/articles/traditional-mexican-dress |
| Scottish kilt | flat overlapping front aprons; side/back pleats; waist fastening; coherent tartan sett through folds | plaid skirt | Heritage Crafts: https://heritagecrafts.org.uk/craft/kilt-making/ |
| Dirndl | fitted bodice or bodice-dress; separate blouse; full gathered skirt; distinct front apron | corset styling or apron dress alone | Universalmuseum Joanneum: https://www.museum-joanneum.at/en/folk-life-museum/our-programme/exhibitions/display-cases-trachtensaal/display-case-8 |
| Bunad | one named documented regional variant with coherent clothing, embroidery, silverwork, and accessories | generic Nordic folk styling cannot select a region | Norwegian Institute of Bunad and Folk Costume: https://bunadogfolkedrakt.no/en/frequently-asked-questions |
| Mongol deel | high collar; asymmetric front overlap; side fastening; long body; broad sash | generic belted robe | UNESCO audiovisual archive: https://www.unesco.org/archives/multimedia/document-2200 |
| Central Asian chapan | open-front long outer robe; lining or quilting; long sleeves; strong edge and cuff treatment | bathrobe or East Asian wrap robe | British Museum: https://www.britishmuseum.org/collection/object/W_2019-6020-2 |
| Dhoti | continuous cloth wrapped at waist and routed between or around legs into distinct lower-body drapes | loose white trousers | V&A Indian embroidery: https://www.vam.ac.uk/articles/indian-embroidery |
| Salwar kameez | separate long tunic and loose/tapered trousers; optional dupatta | long dress plus arbitrary scarf | V&A Indian textiles: https://www.vam.ac.uk/articles/indian-textiles |
| Baju kurung | long loose tunic visibly overlapping a separate skirt or sarong | one continuous dress | Singapore Roots: https://www.roots.gov.sg/ich-landing/ich/making-and-wearing-of-baju-kurung |
| Longyi | broad sewn tube or wrapped cloth; functional waist fold, knot, or tuck; continuous ankle-length lower silhouette | trousers or a skirt with no waist-wrap mechanism | British Museum: https://www.britishmuseum.org/collection/object/A_2007-3013-2 |
| Grand boubou | expansive near-rectangular outer body; very broad sleeve openings; neckline/center focus; coordinated inner layer | dashiki shirt, caftan, or separately named agbada | British Museum: https://www.britishmuseum.org/collection/object/E_Af1934-0307-206 |
| Agbada | voluminous outer robe over distinct long tunic and trousers | a single generic boubou or dashiki | Metropolitan Museum: https://www.metmuseum.org/art/collection/search/832366 |
| Andean poncho | central head opening; broad front/back panels; open side drape; woven panel structure and finished edges | cape, blanket scarf, or hooded plastic rain shell | Metropolitan Museum: https://www.metmuseum.org/art/collection/search/815003 |
| Rebozo | long narrow woven shawl; traceable shoulder/torso route; visible width and fringed ends | unstructured scarf | V&A: https://www.vam.ac.uk/articles/traditional-mexican-dress |
| Chut Thai | one of eight named documented formal styles; internally coherent upper/lower/drape/fastening components | generic gold Thai styling cannot select a type | Queen Sirikit Museum of Textiles: https://qsmtthailand.org/showing/%E0%B8%8A%E0%B8%B8%E0%B8%94%E0%B9%84%E0%B8%97%E0%B8%A2-%E0%B8%88%E0%B8%B2%E0%B8%81%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%AA%E0%B8%B3%E0%B8%99%E0%B8%B1%E0%B8%81%E0%B8%AA%E0%B8%B9%E0%B9%88%E0%B8%A3%E0%B8%B2/ |
| Sámi gákti | context-qualified documented variant; cut, trim, belt, and accessories remain coherent | outsider-invented Arctic costume, borrowed sacred symbolism, or tourist prop | Sámi Parliament responsible-tourism guidance: https://matkailu.samediggi.fi/en/visitor-guidance/ |
| Thobe / thawb | ankle-length straight robe body; coherent neckline, front placket, sleeves, and hem construction | white color alone | British Museum: https://www.britishmuseum.org/collection/object/W_As1967-02-16 |
| Abaya | long open or closed outer robe over an inner layer; readable front, sleeve, edge, and hem construction | black color or head covering alone | Metropolitan Museum: https://www.metmuseum.org/art/collection/search/86243 |

## Textile-technique matrix

| Technique | Observable mechanism | Hard confusion boundary | Source |
| --- | --- | --- | --- |
| Batik | wax-resist boundaries, layered dye penetration, base weave, small crackle variation | hard-edged digital print | UNESCO ICH: https://ich.unesco.org/en/RL/indonesian-batik-00170?RL=00170 |
| Ikat | motifs formed in pre-dyed warp or weft yarns; characteristic softly feathered edge and alignment variation | blurred print applied after weaving | Smithsonian National Museum of Asian Art: https://asia.si.edu/explore-art-culture/collections/search/edanmdm%3Afsg_S2006.23/ |
| Kente | narrow woven strips joined into larger cloth; interwoven geometric blocks and strip-scale construction | generic printed geometric fabric | UNESCO ICH: https://ich.unesco.org/en/RL/craftsmanship-of-traditional-woven-textile-kente-02130 |
| Tartan | ordered warp and weft color sequences over visible twill; coherent sett through folds | generic plaid print | V&A Dundee: https://www.vam.ac.uk/dundee/info/v-a-dundee-presents-a-radical-look-at-a-revolutionary-textile |
| Brocade | supplementary pattern yarns visibly distinct from the ground weave and producing woven relief | metallic surface print | Metropolitan Museum: https://www.metmuseum.org/exhibitions/listings/2017/portable-storage/weaving-techniques |
| Embroidery | visible stitch direction, thread crossings, relief, ground cloth, and local tension | printed embroidery simulation | V&A: https://www.vam.ac.uk/articles/embroidery-styles-an-illustrated-guide |

## Context, condition, and climate

`daily`, `work`, `travel`, `riding`, `military`, `court`, `audience`, `ceremonial`, `ritual`, `festival`, `dance`, `wedding`, `mourning`, `coronation`, and `diplomatic` are occasion modifiers. They never choose a garment without its topology. Likewise `tropical`, `arid`, `high-altitude`, `winter`, `rainy`, and `humid` are compatibility constraints that may affect fiber, layer count, or outerwear but never select a culture.

Condition is orthogonal to authenticity. `newly tailored`, `lived-in`, `work-worn`, `ceremonially maintained`, `heirloom repaired`, `museum conserved`, `faded`, `creased`, `stained`, `frayed`, and `patched` describe present material state. `Museum conserved` does not mean pristine, and `traditional` does not mean ancient, unchanged, ceremonial, or museum-held.

## Cultural-safety and documentation boundary

- Clothing is evidence about a depicted garment, not proof of the wearer's identity.
- A label such as `royal`, `regal`, `rustic`, `mystical`, `tribal`, `indigenous`, or `ethnic` is advisory and cannot activate a named form.
- Chut Thai, bunad, hanfu, and gákti candidates require a named documented form or region before detailed accessory selection.
- Sámi dress is a living identity-bearing practice. The candidate therefore carries a representation guard and must not become an invented tourist costume. The source explicitly warns against fake dress, outsider objectification, and treating private people as props.
- Sources describe garments and techniques; they do not validate generated-image recognition rates. Pixel-level qualification remains a separate saved-image review.
- Documentation fields follow ICOM's garment-recording principle of separating object identification, construction, material, measurements, condition, provenance, and context: https://costume.mini.icom.museum/publications/working-with-clothes/documentation/

## Implemented runtime scope

Candidate dictionary version 1.31 adds 28 garment-system candidates, 20 construction atoms, six garment-specific accessories, six textile-technique textures, and six material-surface candidates. Five randomly selected systems receive reusable hard visual profiles for native-pixel testing: kebaya, qipao, Nivi sari, Andean poncho, and West African grand boubou.

The exact-term profiles enforce connected construction and reject single-cue substitutes. The remaining garments stay advisory candidates until a separate profile has equally specific evidence and paired negatives. This prevents a broad research inventory from becoming unsupported hard routing.
