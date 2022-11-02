import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import com.typesafe.config.ConfigFactory
import akkaHttp.httpClient
import scala.concurrent.Await
import scala.concurrent.duration._
import net.liftweb.json.DefaultFormats
import net.liftweb.json._

/*
* These tests not only test the functionality of the akkaHttp client, but
* also the functionality of the AWS Lambda function that it is calling.
* These tests, test each possible outcome of the response from the lambda.
*/
class LambdaRespTest extends AnyFlatSpec with Matchers {
  behavior of "Lambda Function/Response"
  val confFile = ConfigFactory.load()
  val params = confFile.getConfig("testClient")

  implicit val formats = DefaultFormats
  case class ResponseData(message: String, logs_coded: List[String])

  it should "Find 25 Logs within the Interval" in {
    val myRespData = parse(Await.result(httpClient.sendRequest(params.getString("date"),
                                                               params.getString("start"),
                                                               params.getString("delta")), 5.seconds))

    (myRespData \ "message").extract[String] should equal("Logs Found in the Interval.")
    (myRespData \ "logs_coded").extract[List[String]].length should equal(25)
  }

  it should "Find 0 Logs and return \"Interval not present or No logs in the interval\"" in {
    val myRespData = parse(Await.result(httpClient.sendRequest(params.getString("date"),
                                                                params.getString("invalidIntervalStart"),
                                                                params.getString("invalidIntervalDelta")), 5.seconds))

    (myRespData \ "message").extract[String] should equal("Interval not present or No logs in the interval")
    (myRespData \ "logs_coded").extract[List[String]].length should equal(0)
  }

  it should "Find 0 Logs and return \"Incorrect Date/Format or No Logs For The Date: 2012-07-01\"" in {
    val myRespData = parse(Await.result(httpClient.sendRequest(params.getString("invalidDate"),
                                                                params.getString("start"),
                                                                params.getString("delta")), 5.seconds))

    (myRespData \ "message").extract[String] should equal("Incorrect Date/Format or No Logs For The Date: 2012-07-01")
    (myRespData \ "logs_coded").extract[List[String]].length should equal(0)
  }

  it should "Find 0 Logs and return \"Time input format incorrect. Enter in HH:MM:SS format.\"" in {
    val myRespData = parse(Await.result(httpClient.sendRequest(params.getString("date"),
                                                                params.getString("invalidStartFormat"),
                                                                params.getString("invalidDeltaFormat")), 5.seconds))

    (myRespData \ "message").extract[String] should equal("Time input format incorrect. Enter in HH:MM:SS format.")
    (myRespData \ "logs_coded").extract[List[String]].length should equal(0)
  }

  it should "Find 0 Logs and return \"Incorrect Date/Format or No Logs For The Date: 02-28-2017\"" in {
    val myRespData = parse(Await.result(httpClient.sendRequest(params.getString("invalidDateFormat"),
                                                                params.getString("start"),
                                                                params.getString("delta")), 5.seconds))

    (myRespData \ "message").extract[String] should equal("Incorrect Date/Format or No Logs For The Date: 02-28-2017")
    (myRespData \ "logs_coded").extract[List[String]].length should equal(0)
  }

}